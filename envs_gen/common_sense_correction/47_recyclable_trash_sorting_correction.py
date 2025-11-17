from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 47_recyclable_trash_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        Adds the dustbin as a container and the relevant objects (can, french_fries, small-speaker).
        Adds distractor objects to the scene.
        """
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add the objects to be handled in the task
        self.can = self.add_actor("can", "can")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractor objects to the scene
        distractors = ["pot-with-plant", "toycar", "fluted_block", "book", "alarm-clock"]
        self.add_distractors(distractors)
        
        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        1. Pick can and place into dustbin (wrong action)
        2. Pick can from dustbin and place it back on the table (recovery)
        3. Pick french_fries and place it into dustbin (correct action)
        """
        # First action: pick can and place into dustbin (wrong)
        success = self.pick_and_place(self.can, self.dustbin)
        print("Pick can into dustbin:", success)
        if not success:
            return self.info

        # Recovery action: pick can from dustbin and place back on the table
        success = self.pick_and_place(self.can, self.table)
        print("Recover can to table:", success)
        if not success:
            return self.info

        # Correct action: pick french_fries and place into dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Pick french_fries into dustbin:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        Success conditions:
        - french_fries is in the dustbin
        - can is on the table (after recovery)
        - small_speaker remains on the table (not moved)
        """
        if (self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.can, self.table) and
            self.check_on(self.small_speaker, self.table)):
            return True
        return False
