from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 141_dispose_hazardous_and_container_items_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.fork = self.add_actor("fork", "fork")
        self.markpen = self.add_actor("markpen", "markpen")
        self.knife = self.add_actor("knife", "knife")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add distractor objects
        distractor_list = ["toycar", "book", "shoe", "apple", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of actions for the task"""
        # 1. Pick knife and place into dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Pick and place knife:", success)
        if not success:
            return self.info

        # 2. Pick markpen and place onto purple_block (wrong placement)
        success = self.pick_and_place(self.markpen, self.purple_block)
        print("Pick and place markpen (wrong):", success)
        if not success:
            return self.info

        # 3. Pick markpen from purple_block and place into dustbin (recovery)
        success = self.pick_and_place(self.markpen, self.dustbin)
        print("Pick and place markpen (recovery):", success)
        if not success:
            return self.info

        # 4. Pick shampoo and place into dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Pick and place shampoo:", success)
        if not success:
            return self.info

        # 5. Pick fork and place into dustbin
        success = self.pick_and_place(self.fork, self.dustbin)
        print("Pick and place fork:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all required objects are properly disposed"""
        # Check if all target items are in the dustbin
        if (self.check_on(self.knife, self.dustbin) and
            self.check_on(self.markpen, self.dustbin) and
            self.check_on(self.shampoo, self.dustbin) and
            self.check_on(self.fork, self.dustbin)):
            return True
        return False
