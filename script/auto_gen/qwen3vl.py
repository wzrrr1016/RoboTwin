from transformers import AutoModelForImageTextToText, AutoProcessor
import torch
import os
# default: Load the model on the available device(s)
# model = AutoModelForImageTextToText.from_pretrained(
#     "/home/wangzhuoran/data/MODELS/Qwen/Qwen3-VL-30B-A3B-Instruct", dtype="auto", device_map="auto"
# )
model_path = "/home/wangzhuoran/data0/MODELS/Qwen/Qwen3-VL-8B-Instruct"
# We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    dtype=torch.bfloat16,
    # attn_implementation="flash_attention_2",
    device_map="auto",
)

processor = AutoProcessor.from_pretrained(model_path)

image_path = "/home/wangzhuoran/RoboTwin/robotwin_data/1_toy_and_metal_storage_correction/data_collect/front_camera/episode0/frames_raw/frame_000006.png"
prompt = '''
You are a robot with one robot arm. You are given a task to complete. Output the next action you will take to complete the task.
You have the following actions available, you can choose one of the tools to complete the task:
1. pick_up(object_name, point): pick up the object and the point of the object in the image like (x,y)
2. place(object_name, point): place the object at the point
3. ask_for_help(text): ask for help with the text
4.done(): finish the task

Based on the image and the task, output the next action you will take to complete the task.
Now your task is: do something so that there are more blue blocks on the plate than the red blocks.
'''


task = "Put small lightweight toys onto the plate and metallic or heavy non-toy items into the shoe_box."
prompt = f"Your task is :{task} You need to take the next action based on the current visual observation to complete the task. You can choose from the following actions: 1. pick(obejct_name,points): pick up the objects at the point [x,y];place(container,points): place the held object into the container at point [x,y]; done(). Now output your action."

dir = "/home/wangzhuoran/RoboTwin/robotwin_data/1_toy_and_metal_storage_correction/data_collect/front_camera/episode0/frames_raw"
all_images = os.listdir(dir)
all_images.sort()

for image in all_images:
    image_path = os.path.join(dir, image)

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image_path,
                },
                {"type": "text", "text": prompt},
            ],
        }
    ]

    # Preparation for inference
    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    )
    inputs = inputs.to(model.device)

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=2560)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    print("********\n",output_text)