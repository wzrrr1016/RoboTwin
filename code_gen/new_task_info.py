
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
    "scene: On the table, there are a bottle, a can, a toycar, and an apple. A wooden-box is available. /"
    "task: Place all non-food items into the wooden-box. /"
    "action: Place the bottle, the can, and the toycar in the wooden-box."
}


EXCLUSION_TASK_E = {
    "task_name": "exclusion_task_e",
    "task_description":
    "scene: On the table, there are two cup_without_handle, a bread, a toycar, and an apple. A wooden-box is available. /"
    "task: Place all non-food items into the wooden-box. /"
    "action: First accidentally grasp an apple, and put it back to the table. Place the two cup_without_handle, the can, and the toycar in the wooden-box."
}