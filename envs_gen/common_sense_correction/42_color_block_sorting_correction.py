from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 42_color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Load objects
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.knife = self.add_actor("knife", "knife")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.shampoo = self.add_actor("shampoo", "shampoo")

    def play_once(self):
        # Step 1: Pick purple_block from shoe_box and place into fluted_block
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("pick place purple_block:", success)
        if not success:
            return self.info

        # Step 2: Pick yellow_block and place into shoe_box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

        # Step 3: Pick knife from table and place into shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("pick place knife:", success)
        if not success:
            return self.info

        # Step 4: Pick tissue-box and place into shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("pick place tissue-box:", success)
        if not success:
            return self.info

        # Step 5: Pick shampoo and place into shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("pick place shampoo:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if purple_block is in fluted_block
        if not self.check_on(self.purple_block, self.fluted_block):
            return False

        # Check if yellow_block is in shoe_box
        if not self.check_on(self.yellow_block, self.shoe_box):
            return False

        # Check if knife is in shoe_box
        if not self.check_on(self.knife, self.shoe_box):
            return False

        # Check if tissue-box is in shoe_box
        if not self.check_on(self.tissue_box, self.shoe_box):
            return False

        # Check if shampoo is in shoe_box
        if not self.check_on(self.shampoo, self.shoe_box):
            return False

        return True
