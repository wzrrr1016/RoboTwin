from openai import OpenAI

kimi_api = "Your key"
openai_api = "Your key"
deep_seek_api = "Your key"
local_api = "EMPTY"

# Configure the API and key (using DeepSeek as an example)
def generate(message, gpt="deepseek", temperature=0):

    if gpt == "deepseek":
        MODEL = "deepseek-chat"
        OPENAI_API_BASE = "https://api.deepseek.com"
        # Set your API key here
        OPENAI_API_KEY = deep_seek_api
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    elif gpt == "openai":
        MODEL = "gpt-4o"
        OPENAI_API_BASE = "https://api.gptapi.us/v1"
        OPENAI_API_KEY = openai_api
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    elif gpt == "local":
        MODEL = "/home/wangzhuoran/data4/MODELS/Qwen/Qwen3-32B"
        OPENAI_API_BASE = "http://localhost:8000/v1"
        OPENAI_API_KEY = local_api
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    else:
        raise ValueError(f"Unsupported API provider: {gpt}")

    print('start generating')
    response = client.chat.completions.create(
        model=MODEL,
        messages=message,
        stream=False,
        temperature=temperature,
    )
    print('end generating')

    return response.choices[0].message.content


if __name__ == "__main__":
    message = [{"role": "user", "content": "你好"}]
    print(generate(message, gpt="local"))


