
PICK_PLACE_BLOCK_2R2B = {
    "task_name": "pick_place_block_2r2b",
    "task_description":
    "There are totally 6 blocks with different colors and a plate on the table. Two of them are red, three of them are blue and one of them is green. \
    The task is to pick up some blocks so that there are more blue blocks and red blocks on the plate than on the table. \
    So you need to pick at least 2 red blocks and 2 blue blocks to the plate."
}

PICK_PLACE_BLOCK_COLOR_BALANCE = {
    "task_name": "pick_place_block_color_balance",
    "task_description": "There are 7 blocks on the table: 3 red, 2 blue, 1 yellow, and 1 green. A green bowl is available. \
    Move blocks to the bowl so that the number of red blocks on the table equals the number of blue blocks in the bowl, \
    and the total number of red blocks in the bowl must be odd. You must move exactly 1 red block and all blue blocks."
}

PICK_PLACE_BLOCK_DUAL_CONTAINER = {
    "task_name": "pick_place_block_dual_container",
    "task_description":
    "scene: There are 7 blocks on the table: 2 red, 2 green, 1 blue, 1 yellow, and 1 purple. A green bowl and a yellow bowl are available./"
    "task: Move blocks such that the green bowl contains all primary colors (red/green/blue), and the yellow bowl contains more blocks than the green bowl. Each bowl must have at least one block./"
    "action: Place 1 red block, 1 green block, and 1 blue block in the green bowl. Place 1 red block, 1 green block, 1 yellow block, and 1 purple block in the yellow bowl."
}

PICK_PLACE_BLOCK_DUAL_CONTAINER_1 = {
    "task_name": "pick_place_block_dual_container_1",
    "task_description":
    "scene: There are 5 blocks on the table: 1 red, 1 green, 1 blue, 1 yellow, 1 purple. A green bowl and a yellow bowl are available./"
    "task: Move blocks such that the green bowl contains exactly the red and blue blocks, and the yellow bowl contains exactly the green and yellow blocks. Each bowl must have exactly two blocks./"
    "action: Place the red block and blue block in the green bowl. Place the green block and yellow block in the yellow bowl."
}

PICK_PLACE_BLOCK_DUAL_CONTAINER_2 = {
    "task_name": "pick_place_block_dual_container_2",
    "task_description":
    "scene: There are 4 blocks on the table: 2 orange, 1 pink, 1 purple. A black bowl and a plate are available./"
    "task: Move blocks such that the black bowl contains both orange blocks, and the plate contains the pink and purple blocks. The black bowl must have exactly two blocks./"
    "action: Place both orange blocks in the black bowl. Place the pink block and purple block on the plate."
}

PICK_PLACE_BLOCK_DUAL_CONTAINER_3 = {
    "task_name": "pick_place_block_dual_container_3",
    "task_description":
    "scene: There are 5 blocks on the table: 1 red, 1 green, 1 blue, 1 yellow, 1 purple. A blue bowl and a yellow bowl are available./"
    "task: Move blocks such that the blue bowl contains the red and green blocks, and the yellow bowl contains the blue and yellow blocks. The purple block must remain on the table. Each bowl must have exactly two blocks./"
    "action: Place the red block and green block in the blue bowl. Place the blue block and yellow block in the yellow bowl."
}

SYMMETRICAL_PAIRING = {
    "task_name": "symmetrical_pairing",
    "task_description":
    "scene: On the table, there are two bowls and four items: a bottle, a can, a hamburger, and an apple. The bowls are placed at opposite ends of the table./"
    "task: The items must be placed into the bowls to create two identical sets. Each bowl must contain exactly two items, and the contents of the two bowls must be the same type of items. For example, one valid configuration is placing the bottle and can in one bowl, and the hamburger and apple in the other. Another valid configuration is placing the bottle and hamburger in one bowl, and the can and apple in the other. Any configuration that results in two bowls with identical contents is acceptable./"
    "action: Place the bottle and can in one bowl. Place the hamburger and apple in the other bowl."
}

MEAL_COMPOSITION_CAPACITY = {
    "task_name": "meal_composition_capacity",
    "task_description":
    "scene: On the table, there are a bottle, a can, a hamburg, an apple, a bread, and a toycar. A tray and a bowl are available. The bowl can only hold two items. /"
    "task: Prepare a complete meal on the tray. A complete meal is defined as one drink, one main course, and one side item. The remaining items that are not part of the meal must be placed in the bowl. The bowl must be filled to its exact capacity. /"
    "action: Place the bottle, hamburg, and apple on the tray. Place the can and bread in the bowl. The toycar is left on the table."
}

ODD_EVEN_SORT = {
    "task_name": "odd_even_sort",
    "task_description":
    "scene: On the table, there are 3 bottles, 2 cans, and 1 toycar. A tray and a shoe-box are available. /"
    "task: Place all items with an odd quantity into the shoe-box. Place all items with an even quantity onto the tray. /"
    "action: Place the 3 bottles and 1 toycar in the shoe-box. Place the 2 cans on the tray."
}

EXCLUSION_TASK = {
    "task_name": "exclusion_task",
    "task_description":
    "scene: On the table, there are a bottle, a can, a toycar, and an apple. A wooden_box is available. /"
    "task: Place all non-food items into the wooden_box. /"
    "action: Place the bottle, the can, and the toycar in the wooden_box."
}


EXCLUSION_TASK_E = {
    "task_name": "exclusion_task_e",
    "task_description":
    "scene: On the table, there are two cup_without_handle, a bread, a toycar, and an apple. A wooden_box is available. /"
    "task: Place all non-food items into the wooden_box. /"
    "action: First accidentally grasp an apple, and put it back to the table. Place the two cup_without_handle, the can, and the toycar in the wooden_box."
}

# Variants with explicit reasoning steps
EXCLUSION_TASK_E1 = {
    "task_name": "exclusion_task_e1",
    "task_description":
    "scene: On the table, there are two bottles, a can, a toycar, and an apple. A wooden_box is available. /"
    "task: Place all non-food items into the wooden_box. /"
    "action: Intentionally pick up the apple and place it back on the table. Then place both bottles, the can, and the toycar into the wooden_box."
}

EXCLUSION_TASK_E2 = {
    "task_name": "exclusion_task_e2",
    "task_description":
    "scene: On the table, there are two cup_without_handle, a toycar, an apple, and a bread. A wooden_box is available. /"
    "task: Place all non-food items into the wooden_box. /"
    "action: First move the bread and return it to the table as a reasoning step. Then place both cups and the toycar into the wooden_box."
}

EXCLUSION_TASK_E3 = {
    "task_name": "exclusion_task_e3",
    "task_description":
    "scene: On the table, there are a bottle, a can, a toycar, an apple, and a bread. A wooden_box is available. /"
    "task: Place all non-food items into the wooden_box. /"
    "action: Intentionally pick up the apple and put it back on the table. Then place the bottle, the can, and the toycar into the wooden_box."
}

# New reasoning tasks with mistake-and-recovery
SORT_FOOD_NONFOOD_RECOVER = {
    "task_name": "sort_food_nonfood_recover",
    "task_description":
    "scene: On the table are a tray, a shoe-box, and a dustbin. Objects include an apple, a hamburg, a bottle, and a can. /"
    "task: Sort food items onto the tray and non-food items into the shoe-box. Include mistakes and recoveries. /"
    "action: Put the apple in the dustbin by mistake, then move it to the tray. Place the hamburg on the tray. Place the bottle in the shoe-box. Put the can on the tray by mistake, then move it to the shoe-box."
}

MEAL_ASSEMBLY_RECOVER = {
    "task_name": "meal_assembly_recover",
    "task_description":
    "scene: A tray and a shoe-box are available. Objects include french-fries, a hamburg, a fruit, and a calculator. /"
    "task: Assemble a meal (fries, hamburg, fruit) on the tray. Non-food items go to the shoe-box. Include mistakes and recoveries. /"
    "action: Put the calculator on the tray by mistake, then move it to the shoe-box. Put the fruit in the shoe-box by mistake, then move it to the tray. Finally place french-fries and hamburg on the tray."
}

TOOL_AND_DRINK_SEPARATION_RECOVER = {
    "task_name": "tool_and_drink_separation_recover",
    "task_description":
    "scene: A bowl and a plate are available. Objects include a hammer, a microphone, a bottle, and a cup_with_handle. /"
    "task: Place drinks (bottle, cup) into the bowl and tools (hammer, microphone) on the plate. Include mistakes and recoveries. /"
    "action: Put the bottle on the plate by mistake, then move it to the bowl. Place the cup in the bowl. Put the hammer in the bowl by mistake, then move it to the plate. Place the microphone on the plate."
}

CUP_SORTING_SPILL_RECOVER = {
    "task_name": "cup_sorting_spill_recover",
    "task_description":
    "scene: A fluted-block and a wooden_box are available. Objects include cup_with_handle, cup_without_handle, and cup-with-liquid. /"
    "task: Place dry cups into the wooden_box and the cup-with-liquid onto the fluted-block. Include mistakes and recoveries. /"
    "action: Move the cup-with-liquid to the wooden_box by mistake, then move it to the fluted-block. Place the cup_with_handle and cup_without_handle into the wooden_box."
}

RECYCLE_SORT_RECOVER = {
    "task_name": "recycle_sort_recover",
    "task_description":
    "scene: A dustbin and a wooden_box are available. Objects include a can, a bottle, and a pot-with-plant. /"
    "task: Place recyclables (can, bottle) into the dustbin and non-recyclables (pot-with-plant) into the wooden_box. Include mistakes and recoveries. /"
    "action: Put the pot-with-plant into the dustbin by mistake, then move it to the wooden_box. Place the can and bottle into the dustbin."
}

MIXED_CONTAINER_LOGIC_RECOVER = {
    "task_name": "mixed_container_logic_recover",
    "task_description":
    "scene: A bowl, a plate, and a tray are available. Objects include an apple, a hamburg, and a hammer. /"
    "task: Place the apple into the bowl, the hamburg onto the tray, and the hammer onto the plate. Include mistakes and recoveries. /"
    "action: Put the hammer onto the tray by mistake, then move it to the plate. Place the apple into the bowl and the hamburg onto the tray."
}

# Counting reasoning - no correction
COUNT_BLUE_RED_TO_PLATE = {
    "task_name": "count_blue_red_to_plate",
    "task_description":
    "scene: There is a plate on the table and several colored blocks. /"
    "task: Place exactly two red blocks and two blue blocks onto the plate. /"
    "action: Identify red and blue blocks and place any two red and two blue on the plate."
}

# Counting reasoning - with correction
SPLIT_EVEN_ODD_BETWEEN_TRAY_BOWL = {
    "task_name": "split_even_odd_between_tray_bowl",
    "task_description":
    "scene: A tray and a bowl are available with several numbered blocks. /"
    "task: Place even-numbered blocks into the bowl and odd-numbered blocks onto the tray. Include a mistake and recovery. /"
    "action: Put an odd block into the bowl by mistake, then move it to the tray. Finally, place all even blocks into the bowl and all odd blocks onto the tray."
}

ENSURE_MAJORITY_IN_WOODEN_BOX = {
    "task_name": "ensure_majority_in_wooden_box",
    "task_description":
    "scene: A wooden_box and a plate are available with five blocks. /"
    "task: Ensure the majority of blocks are in the wooden_box, with a mistake and recovery. /"
    "action: Place two blocks on the plate by mistake, then move one back to the wooden_box. Place the remaining blocks into the wooden_box to ensure at least three blocks are inside."
}

# Common-sense - no correction
TOOL_DRINK_PLACEMENT = {
    "task_name": "tool_drink_placement",
    "task_description":
    "scene: A bowl and a plate are available with a hammer, a microphone, a bottle, and a cup. /"
    "task: Place tools on the plate and drinks in the bowl (no corrections). /"
    "action: Place the hammer and microphone on the plate; place the bottle and cup in the bowl."
}

# Spatial reasoning - no correction (simplified left/right)
PLACE_FOOD_LEFT_TOOLS_RIGHT = {
    "task_name": "place_food_left_tools_right",
    "task_description":
    "scene: A tray is available with two food items (apple, hamburg) and two tools (hammer, microphone). /"
    "task: Place food on the left side of the tray and tools on the right (no corrections). /"
    "action: Place all four items on the tray with the intent of left/right separation for food/tools."
}
