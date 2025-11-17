from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 352_dispose_recyclables_and_disposables_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add target objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.can = self.add_actor("can", "can")
        self.bottle = self.add_actor("bottle", "bottle")
        self.bell = self.add_actor("bell", "bell")
        
        # Add distractors
        distractor_list = ["battery", "apple", "alarm-clock", "red_block", "screwdriver"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # 1. Put tissue-box in dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Tissue-box placed:", success)
        if not success:
            return self.info

        # 2. Put can in dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Can placed:", success)
        if not success:
            return self.info

        # 3. Wrong action: Put bell in dustbin
        success = self.pick_and_place(self.bell, self.dustbin)
        print("Bell placed in dustbin (wrong):", success)
        if not success:
            return self.info

        # 4. Recovery: Put bell on table
        success = self.pick_and_place(self.bell, self.table)
        print("Bell placed on table (recovery):", success)
        if not success:
            return self.info

        # 5. Put bottle in dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Bottle placed:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all task requirements are met"""
        return (
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.bell, self.table)
        )
