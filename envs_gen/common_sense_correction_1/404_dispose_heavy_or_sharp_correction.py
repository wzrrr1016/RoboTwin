from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 404_dispose_heavy_or_sharp_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required objects and distractors in the environment"""
        # Create main containers and objects
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.knife = self.add_actor("knife", "knife")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "alarm-clock", "tissue-box", "book", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions for the task"""
        # 1. Wrong action: Place food item in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Place french fries into dustbin (wrong):", success)
        if not success:
            return self.info

        # 2. Recovery: Move food item to proper location
        success = self.pick_and_place(self.french_fries, self.blue_block)
        print("Recover french fries to blue block:", success)
        if not success:
            return self.info

        # 3. Discard heavy item
        success = self.pick_and_place(self.dumbbell, self.dustbin)
        print("Place dumbbell into dustbin:", success)
        if not success:
            return self.info

        # 4. Discard sharp item
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Place knife into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if food is on blue block (not in dustbin)
        # Check if heavy and sharp items are in dustbin
        return (
            self.check_on(self.french_fries, self.blue_block) and
            self.check_on(self.dumbbell, self.dustbin) and
            self.check_on(self.knife, self.dustbin)
        )
