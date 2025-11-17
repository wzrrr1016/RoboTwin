from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 152_store_toys_and_keep_foods_tools_out_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the simulation environment"""
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects to be manipulated
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.drill = self.add_actor("drill", "drill")
        self.apple = self.add_actor("apple", "apple")
        
        # Add distractor objects
        distractor_list = ['pot-with-plant', 'alarm-clock', 'book', 'shoe', 'microphone']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions for the task"""
        # Place blue block into shoe box
        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # Wrongly place apple into shoe box (needs recovery)
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Place apple (wrong):", success)
        if not success:
            return self.info

        # Recovery: pick apple from shoe box and place on table
        success = self.pick_and_place(self.apple, self.table)
        print("Recover apple:", success)
        if not success:
            return self.info

        # Place yellow block into shoe box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        # Place drill on table (not in box)
        success = self.pick_and_place(self.drill, self.table)
        print("Place drill on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if blocks are in the box
        blocks_in_box = (
            self.check_on(self.blue_block, self.shoe_box) and 
            self.check_on(self.yellow_block, self.shoe_box)
        )
        
        # Check if restricted items are outside the box
        items_outside_box = (
            self.check_on(self.apple, self.table) and 
            self.check_on(self.drill, self.table)
        )
        
        return blocks_in_box and items_outside_box
