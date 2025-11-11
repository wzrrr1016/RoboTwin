from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 6_discard_perishable_keep_reusables_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add the main objects
        self.book = self.add_actor("book", "book")
        self.mug = self.add_actor("mug", "mug")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add distractor objects
        distractor_list = ["screwdriver", "hammer", "toycar", "alarm-clock", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's actions for the task"""
        # 1. Place oily food waste (french fries) in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Place french_fries into dustbin:", success)
        if not success:
            return self.info

        # 2. Wrong action: Place mug in dustbin
        success = self.pick_and_place(self.mug, self.dustbin)
        print("Wrongly place mug into dustbin:", success)
        if not success:
            return self.info

        # 3. Recovery: Move mug back to table
        success = self.pick_and_place(self.mug, self.table)
        print("Recover mug to table:", success)
        if not success:
            return self.info

        # 4. Place book on table
        success = self.pick_and_place(self.book, self.table)
        print("Place book on table:", success)
        if not success:
            return self.info

        # 5. Place shampoo on table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Place shampoo on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if oily food waste is in dustbin
        if not self.check_on(self.french_fries, self.dustbin):
            return False
            
        # Check if reusable items are NOT in dustbin
        if self.check_on(self.mug, self.dustbin):
            return False
        if self.check_on(self.book, self.dustbin):
            return False
        if self.check_on(self.shampoo, self.dustbin):
            return False
            
        # Check if items are properly placed on table
        if not self.check_on(self.mug, self.table):
            return False
        if not self.check_on(self.book, self.table):
            return False
        if not self.check_on(self.shampoo, self.table):
            return False
            
        return True
