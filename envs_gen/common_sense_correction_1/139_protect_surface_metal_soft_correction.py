from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 139_protect_surface_metal_soft_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the coaster as a container.
        - Add the required objects: dumbbell, small-speaker, bell, tissue-box.
        - Add distractor objects as specified in the task description.
        """
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add the required objects
        self.dumbbell = self.add_actor("dumbbell", "dumbbell_0")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker_0")
        self.bell = self.add_actor("bell", "bell_0")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box_0")
        
        # Add distractor objects
        distractor_list = ["apple", "baguette", "bread", "french_fries", "hamburg"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm to complete the task.
        Steps:
        1. Place dumbbell on coaster.
        2. Place tissue-box on coaster (wrong action).
        3. Place tissue-box back on table (recovery).
        4. Place bell on coaster.
        5. Place small-speaker on table.
        """
        # Step 1: Place dumbbell on coaster
        success = self.pick_and_place(self.dumbbell, self.coaster)
        print("Dumbbell to coaster:", success)
        if not success:
            return self.info

        # Step 2: Place tissue-box on coaster (wrong action)
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("Tissue-box to coaster (wrong):", success)
        if not success:
            return self.info

        # Step 3: Place tissue-box back on table (recovery)
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Tissue-box to table (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place bell on coaster
        success = self.pick_and_place(self.bell, self.coaster)
        print("Bell to coaster:", success)
        if not success:
            return self.info

        # Step 5: Place small-speaker on table
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Small-speaker to table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        - Hard/metal items (dumbbell, bell) must be on the coaster.
        - Soft paper (tissue-box) and electronic (small-speaker) items must be on the table.
        """
        if (self.check_on(self.dumbbell, self.coaster) and
            self.check_on(self.bell, self.coaster) and
            self.check_on(self.tissue_box, self.table) and
            self.check_on(self.small_speaker, self.table)):
            return True
        return False
