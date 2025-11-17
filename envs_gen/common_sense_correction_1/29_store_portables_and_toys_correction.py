from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 29_store_portables_and_toys_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Add the shoe_box as the target container.
        - Add the relevant objects: small-speaker (portable electronics), orange_block (small toy), 
          bottle, and cup_with_handle.
        - Add distractor objects as specified in the task description.
        """
        # Add the shoe box as the container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add the relevant objects
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")

        # Add distractor objects
        distractor_list = ['pot-with-plant', 'dumbbell', 'book', 'baguette', 'tissue-box']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Pick and place the small-speaker into the shoe_box.
        - Pick and place the orange_block into the shoe_box.
        - If any action fails, return early to stop further execution.
        """
        # Pick and place the small speaker into the shoe box
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Pick small-speaker:", success)
        if not success:
            return self.info

        # Pick and place the orange block into the shoe box
        success = self.pick_and_place(self.orange_block, self.shoe_box)
        print("Pick orange_block:", success)
        if not success:
            return self.info

        # Return the final state
        return self.info

    def check_success(self):
        """
        Check if the task was successfully completed.
        - The small-speaker and orange_block must be placed into the shoe_box.
        - Use the `check_on` API to verify if the objects are on the container.
        """
        # Check if both objects are on the shoe box
        if self.check_on(self.small_speaker, self.shoe_box) and self.check_on(self.orange_block, self.shoe_box):
            return True
        return False
