from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 23_recyclables_and_toys_sorting_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the simulation environment"""
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects to be manipulated
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.green_block = self.add_actor("green_block", "green_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        
        # Add distractor objects
        distractor_list = ["calculator", "hammer", "stapler", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # 1. Place green_block in shoe_box
        success = self.pick_and_place(self.green_block, self.shoe_box)
        print("Place green_block into shoe_box:", success)
        if not success:
            return self.info
            
        # 2. Wrong placement: can in shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Place can into shoe_box (wrong):", success)
        if not success:
            return self.info
            
        # 3. Recovery: move can from shoe_box to dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Recover can to dustbin:", success)
        if not success:
            return self.info
            
        # 4. Place bottle in dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Place bottle into dustbin:", success)
        if not success:
            return self.info
            
        # 5. Place orange_block in shoe_box
        success = self.pick_and_place(self.orange_block, self.shoe_box)
        print("Place orange_block into shoe_box:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        return (
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.green_block, self.shoe_box) and
            self.check_on(self.orange_block, self.shoe_box)
        )
