from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 87_store_toys_and_reading_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the environment.
        - Containers: wooden_box
        - Objects: yellow_block, small-speaker, mouse, book
        - Distractors: apple, shoe, pot-with-plant, hammer, shampoo
        """
        # Add the wooden box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add the required objects
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.mouse = self.add_actor("mouse", "mouse")
        self.book = self.add_actor("book", "book")

        # Add distractor objects
        distractor_list = ["apple", "shoe", "pot-with-plant", "hammer", "shampoo"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions:
        1. Pick yellow_block and place it into wooden_box
        2. Pick small-speaker and place it into wooden_box (wrong action)
        3. Pick small-speaker from wooden_box and place it on mouse (recovery)
        4. Pick book and place it into wooden_box
        """
        # Step 1: Place yellow_block into wooden_box
        success = self.pick_and_place(self.yellow_block, self.wooden_box)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place small-speaker into wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Place small-speaker (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing small-speaker on mouse
        success = self.pick_and_place(self.small_speaker, self.mouse)
        print("Recover small-speaker:", success)
        if not success:
            return self.info

        # Step 4: Place book into wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Place book:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if the task is successfully completed:
        - yellow_block is on wooden_box
        - book is on wooden_box
        """
        if self.check_on(self.yellow_block, self.wooden_box) and self.check_on(self.book, self.wooden_box):
            return True
        return False
