from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 132_hygiene_food_and_toys_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractors
        distractor_list = ['pot-with-plant', 'book', 'pet-collar', 'sand-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrong action - Put apple in wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Wrong action - apple to wooden_box:", success)
        if not success:
            return self.info

        # Step 2: Recovery - Put apple in shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Recovery - apple to shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Put shampoo in shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Shampoo to shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Put blue_block in wooden_box
        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("Blue block to wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Put red_block in wooden_box
        success = self.pick_and_place(self.red_block, self.wooden_box)
        print("Red block to wooden_box:", success)
        if not success:
            return self.info

        # Step 6: Put knife in wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Knife to wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all items are in their correct containers
        if (
            self.check_on(self.apple, self.shoe_box) and
            self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.blue_block, self.wooden_box) and
            self.check_on(self.red_block, self.wooden_box) and
            self.check_on(self.knife, self.wooden_box)
        ):
            return True
        return False
