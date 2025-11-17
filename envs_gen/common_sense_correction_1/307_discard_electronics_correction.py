from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 307_discard_electronics_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes containers, target objects, and distractors.
        """
        # Add the dustbin as a container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add electronic devices to be placed in the dustbin
        self.mouse = self.add_actor("mouse", "mouse")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add non-electronic object (blue_block) for the recovery step
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add hammer for the recovery step
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractors to the environment
        distractor_list = ["apple", "baguette", "shoe", "book", "pot-with-plant", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        Includes placing electronic devices in the dustbin and recovery of a wrongly placed object.
        """
        # Step 1: Pick mouse and place it into dustbin
        success = self.pick_and_place(self.mouse, self.dustbin)
        print("Pick mouse:", success)
        if not success:
            return self.info

        # Step 2: Pick blue_block and place it into dustbin (wrong action)
        success = self.pick_and_place(self.blue_block, self.dustbin)
        print("Pick blue_block (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick blue_block from dustbin and place it onto hammer (recovery)
        success = self.pick_and_place(self.blue_block, self.hammer)
        print("Recover blue_block:", success)
        if not success:
            return self.info

        # Step 4: Pick small-speaker and place it into dustbin
        success = self.pick_and_place(self.small_speaker, self.dustbin)
        print("Pick small-speaker:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task is successfully completed.
        The success condition is:
        - Mouse and small-speaker are in the dustbin
        - Blue_block is on the hammer (not in the dustbin)
        """
        if (
            self.check_on(self.mouse, self.dustbin) and
            self.check_on(self.small_speaker, self.dustbin) and
            self.check_on(self.blue_block, self.hammer)
        ):
            return True
        return False
