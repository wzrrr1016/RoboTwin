from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 432_dispose_food_and_single_use_hygiene_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the dustbin as a container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add the target objects to be manipulated
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractor objects to the environment
        distractor_list = ["hammer", "toycar", "pot-with-plant", "dumbbell", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm to complete the task.
        """
        # Step 1: Pick and place french_fries into dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Place french fries:", success)
        if not success:
            return self.info

        # Step 2: Pick and place small-speaker into dustbin (wrong action)
        success = self.pick_and_place(self.small_speaker, self.dustbin)
        print("Wrongly place small speaker:", success)
        if not success:
            return self.info

        # Step 3: Pick and place small-speaker back on the table (recovery)
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Recover small speaker:", success)
        if not success:
            return self.info

        # Step 4: Pick and place tissue-box into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Place tissue box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking the final positions of objects.
        """
        # Task success conditions:
        # 1. french_fries is in the dustbin
        # 2. tissue_box is in the dustbin
        # 3. small_speaker is on the table (not in the dustbin)
        if (self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.small_speaker, self.table)):
            return True
        return False
