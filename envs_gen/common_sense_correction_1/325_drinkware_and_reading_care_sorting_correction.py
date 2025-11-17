from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 325_drinkware_and_reading_care_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Containers: wooden_box, fluted_block
        - Objects: mug, bottle, shampoo, book
        - Distractors: calculator, hammer, toycar, pot-with-plant, small-speaker
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.bottle = self.add_actor("bottle", "bottle")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.book = self.add_actor("book", "book")

        # Add distractors
        distractor_list = ["calculator", "hammer", "toycar", "pot-with-plant", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - First, place the bottle into the wooden_box (wrong action).
        - Then, recover by placing the bottle onto the fluted_block.
        - Place the mug onto the fluted_block.
        - Place the shampoo and book into the wooden_box.
        """
        # Wrong action: place bottle into wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Wrong action - place bottle into wooden_box:", success)
        if not success:
            return self.info

        # Recovery: move bottle to fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Recovery - place bottle onto fluted_block:", success)
        if not success:
            return self.info

        # Place mug onto fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug onto fluted_block:", success)
        if not success:
            return self.info

        # Place shampoo into wooden_box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Place shampoo into wooden_box:", success)
        if not success:
            return self.info

        # Place book into wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Place book into wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if all objects are placed in the correct containers:
        - Drinkware (bottle, mug) on fluted_block
        - Reading (book) and personal-care (shampoo) items in wooden_box
        """
        if (self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.shampoo, self.wooden_box) and
            self.check_on(self.book, self.wooden_box)):
            return True
        return False
