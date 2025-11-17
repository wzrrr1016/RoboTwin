from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 280_store_liquids_and_blocks_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.mug = self.add_actor("mug", "mug")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")

        # Add distractors
        distractor_list = ["calculator", "battery", "screwdriver", "alarm-clock", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick bottle and place into wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Pick and place bottle:", success)
        if not success:
            return self.info

        # Step 2: Pick yellow_block and place into wooden_box (wrong)
        success = self.pick_and_place(self.yellow_block, self.wooden_box)
        print("Pick and place yellow_block (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick yellow_block from wooden_box and place into shoe_box (recovery)
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Recover yellow_block to shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Pick purple_block and place into shoe_box
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("Pick and place purple_block:", success)
        if not success:
            return self.info

        # Step 5: Pick mug and place into wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Pick and place mug:", success)
        if not success:
            return self.info

        # Step 6: Pick shampoo and place into wooden_box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Pick and place shampoo:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all liquid/personal-care items are in wooden_box
        bottle_in_wooden = self.check_on(self.bottle, self.wooden_box)
        mug_in_wooden = self.check_on(self.mug, self.wooden_box)
        shampoo_in_wooden = self.check_on(self.shampoo, self.wooden_box)

        # Check if blocks are in shoe_box
        yellow_in_shoe = self.check_on(self.yellow_block, self.shoe_box)
        purple_in_shoe = self.check_on(self.purple_block, self.shoe_box)

        return (bottle_in_wooden and mug_in_wooden and shampoo_in_wooden and
                yellow_in_shoe and purple_in_shoe)
