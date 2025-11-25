from typing import Dict, List
# Extended attribute knowledge base
ATTR_KB: Dict[str, List[str]] = {
    # foods and nutrition
    "apple": ["food", "healthy", "red", "round", "natural", "fruit", "edible", "organic", "perishable"],
    "bread": ["food", "fermented", "grain", "carbohydrate", "edible", "soft", "perishable"],
    "hamburg": ["food", "unhealthy", "has_bread", "fermented", "contains_meat", "processed", "fast_food", "edible"],
    "french_fries": ["food", "unhealthy", "fried", "yellow", "fast_food", "hot", "oily", "edible"],

    # drinkware / liquid holders and handles
    "bottle": ["liquid_container", "no_handle", "transparent", "plastic_or_glass", "portable", "drinkware", "recyclable"],
    "cup": ["liquid_container", "unknown_handle", "drinkware", "for_drinking"],
    "cup_with_handle": ["liquid_container", "has_handle", "drinkware", "for_hot_drinks", "easy_to_hold"],
    "cup_without_handle": ["liquid_container", "no_handle", "drinkware", "for_cold_drinks", "hard_to_hold_when_hot"],
    "mug": ["liquid_container", "has_handle", "drinkware", "for_hot_drinks", "ceramic"],
    "can": ["liquid_container", "metal", "no_handle", "sealed", "cylindrical", "drinkware", "recyclable"],

    # tableware and danger
    "knife": ["tableware", "dangerous", "sharp", "metal", "cutting_tool", "requires_care"],
    "fork": ["tableware", "metal", "for_eating", "has_prongs", "safe"],

    # tools / repair / office
    "screwdriver": ["tool", "repair", "metal", "hand_tool", "for_screws", "maintenance"],
    "drill": ["tool", "repair", "electric", "power_tool", "for_holes", "maintenance", "heavy"],
    "stapler": ["tool", "office", "metal", "for_paper", "binding_tool"],
    "scanner": ["electronic", "office", "for_documents", "digital", "stationary"],
    "mouse": ["electronic", "office", "computer_accessory", "plastic", "handheld"],
    "hammer": ["tool", "repair", "metal", "hand_tool", "for_striking", "heavy"],

    # toys / decor
    "toycar": ["toy", "wheels", "for_children", "entertainment", "movable", "plastic"],
    "pot-with-plant": ["plant", "decor", "green", "living", "needs_water", "decorative", "natural", "organic"],

    # time / sound utilities
    "alarm-clock": ["time", "sound", "electronic", "wakes_up", "displays_time", "makes_noise"],
    "sand-clock": ["time", "no_sound", "analog", "visual", "passive", "decorative"],
    "microphone": ["sound", "audio_input", "electronic", "for_recording", "captures_sound"],
    "bell": ["sound", "audio_output", "metal", "for_alerting", "produces_sound", "ringing"],
    "small-speaker": ["sound", "audio_output", "electronic", "for_music", "produces_sound", "portable"],

    # cleaning / bath / weight
    "tissue-box": ["cleaning", "paper", "disposable", "for_wiping", "hygiene", "single_use", "recyclable"],
    "shampoo": ["bath", "liquid", "hygiene", "for_hair", "personal_care", "consumable", "bottle_container"],
    "dumbbell": ["heavy", "metal", "exercise", "fitness", "weight_training", "solid"],

    # clothing
    "shoe": ["clothing", "footwear", "wearable", "protective", "for_feet", "outdoor"],

    # reading / material
    "book": ["reading", "wood_material", "paper", "educational", "rectangular", "has_pages", "knowledge", "recyclable"],
    "teanet": ["tea", "kitchen", "for_tea", "mesh", "strainer"],


    "markpen": ["writing_tool", "for_marking", "black", "ink_based", "stationery"],

    # colored square blocks (RGB color model)
    "red_block": ["block", "red", "primary_color", "square", "solid", "toy_or_tool"],
    "green_block": ["block", "green", "primary_color", "square", "solid", "toy_or_tool"],
    "blue_block": ["block", "blue", "primary_color", "square", "solid", "toy_or_tool"],
    "yellow_block": ["block", "yellow", "secondary_color", "square", "solid", "toy_or_tool"],
    "purple_block": ["block", "purple", "secondary_color", "square", "solid", "toy_or_tool"],
    "orange_block": ["block", "orange", "tertiary_color", "square", "solid", "toy_or_tool"],
    "pink_block": ["block", "pink", "tint", "square", "solid", "toy_or_tool"],
}

# Container attributes
CONTAINER_KB: Dict[str, List[str]] = {
    "plate": ["container", "food_surface", "flat", "circular", "for_food", "kitchen", "ceramic","cicular"],
    "tray": ["container", "group_surface", "flat", "rectangular", "for_organization", "holds_multiple_items","rectangle"],
    "wooden_box": ["container", "storage", "enclosed", "wood", "for_general_items", "has_lid","rectangular"],
    "dustbin": ["container", "waste", "for_trash", "disposal", "unwanted_items", "recyclable_items"],
    "shoe_box": ["container", "for_shoe", "enclosed", "specific_purpose", "storage", "rectangular"],
    "coaster": ["container", "for_drinkware", "flat", "protects_surface", "for_cups_and_mugs", "circular"],
}

DISTRACTOR_KB: Dict[str, List[str]] = {
    "calculator": ["electronic", "office", "for_calculation", "digital", "handheld", "rectangular", "battery_powered"],
    "cup-with-liquid": ["liquid_container", "drinkware", "has_liquid", "filled", "needs_care", "spillable"],
    "chips-tub": ["food", "snack", "unhealthy", "packaged", "plastic_container", "sealed", "lightweight"],
    "pet-collar": ["pet_accessory", "wearable", "for_animals", "strap", "adjustable", "safety"],
    "table-tennis": ["sport", "ball", "round", "lightweight", "white", "small", "bouncy"],
    "roll-paper": ["paper", "disposable", "hygiene", "for_cleaning", "cylindrical", "single_use", "absorbent"],
    "olive-oil": ["liquid", "cooking", "kitchen", "healthy", "edible", "bottle_container", "consumable"],
    "jam-jar": ["food", "sweet", "glass_container", "sealed", "spreadable", "preserved", "edible"],
    "milk-box": ["liquid", "food", "dairy", "carton", "rectangular", "perishable", "drinkware", "nutritious"],
    "baguette": ["food", "bread", "long", "french", "grain", "edible", "carbohydrate", "perishable"],
    "battery": ["electronic", "power_source", "cylindrical", "metal", "portable", "energy_storage", "recyclable"],
    "msg": ["seasoning", "powder", "cooking", "kitchen", "flavor_enhancer", "white", "edible"],
    "soy-sauce": ["liquid", "seasoning", "cooking", "kitchen", "salty", "bottle_container", "dark", "edible"],
    "fluted_block": ["block", "toy", "square","solid"],
}

for obj in ATTR_KB.keys():
    DISTRACTOR_KB[obj] = ATTR_KB[obj]
