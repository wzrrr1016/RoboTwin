from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 179_dispose_disposables_and_food_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add main objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.mug = self.add_actor("mug", "mug")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "pot-with-plant", "alarm-clock", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of actions for the task"""
        # 1. Pick tissue-box and place it into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Tissue box to dustbin:", success)
        if not success:
            return self.info

        # 2. Pick mug and place it into dustbin (wrong action)
        success = self.pick_and_place(self.mug, self.dustbin)
        print("Mug to dustbin (wrong):", success)
        if not success:
            return self.info

        # 3. Pick mug from dustbin and place it back on the table (recovery)
        success = self.pick_and_place(self.mug, self.table)
        print("Mug back to table:", success)
        if not success:
            return self.info

        # 4. Pick hamburg and place it into dustbin
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Hamburg to dustbin:", success)
        if not success:
            return self.info

        # 5. Pick fork and place it on the table
        success = self.pick_and_place(self.fork, self.table)
        print("Fork to table:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check disposable items in dustbin
        tissue_in_dustbin = self.check_on(self.tissue_box, self.dustbin)
        food_in_dustbin = self.check_on(self.hamburg, self.dustbin)
        
        # Check reusable items not in dustbin
        mug_not_in_dustbin = not self.check_on(self.mug, self.dustbin)
        fork_not_in_dustbin = not self.check_on(self.fork, self.dustbin)
        
        return all([
            tissue_in_dustbin,
            food_in_dustbin,
            mug_not_in_dustbin,
            fork_not_in_dustbin
        ])
