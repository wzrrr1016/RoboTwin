from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 389_waste_and_storage_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: dustbin, wooden_box
        - Objects: can, tissue-box, book, stapler
        - Distractors: pot-with-plant, toycar, red_block, blue_block, shoe
        """
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects to be manipulated
        self.can = self.add_actor("can", "can")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.book = self.add_actor("book", "book")
        self.stapler = self.add_actor("stapler", "stapler")

        # Add distractor objects
        distractor_list = ['pot-with-plant', 'toycar', 'red_block', 'blue_block', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions to complete the task:
        1. Place tissue-box into dustbin
        2. Place book into dustbin (wrong action)
        3. Recover book by placing it into wooden_box
        4. Place can into dustbin
        5. Place stapler into wooden_box
        """
        # Step 1: Place tissue-box into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Place tissue-box into dustbin:", success)
        if not success:
            return self.info

        # Step 2: Place book into dustbin (wrong action)
        success = self.pick_and_place(self.book, self.dustbin)
        print("Place book into dustbin (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover book by placing it into wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Recover book to wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place can into dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Place can into dustbin:", success)
        if not success:
            return self.info

        # Step 5: Place stapler into wooden_box
        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("Place stapler into wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying:
        - Tissue-box and can are in the dustbin
        - Book and stapler are in the wooden_box
        """
        if (
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.book, self.wooden_box) and
            self.check_on(self.stapler, self.wooden_box)
        ):
            return True
        return False
