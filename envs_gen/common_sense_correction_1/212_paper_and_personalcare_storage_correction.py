from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 212_paper_and_personalcare_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        """
        # Add the wooden box as the target container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add the objects to be manipulated
        self.book = self.add_actor("book", "book")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.hammer = self.add_actor("hammer", "hammer")

        # Add distractor objects to the environment
        distractor_list = ["shoe", "dumbbell", "alarm-clock", "toycar", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        """
        # Step 1: Pick and place the book into the wooden box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Pick place book:", success)
        if not success:
            return self.info

        # Step 2: Pick and place the tissue box into the wooden box
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("Pick place tissue-box:", success)
        if not success:
            return self.info

        # Step 3: Pick and place the french fries into the wooden box (wrong action)
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("Pick place french_fries (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover by picking the french fries from the wooden box and placing it on the table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Recover french_fries to table:", success)
        if not success:
            return self.info

        # Step 5: Pick and place the shampoo into the wooden box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Pick place shampoo:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of the objects.
        """
        # The task is successful if the book, tissue-box, and shampoo are in the wooden box
        return (
            self.check_on(self.book, self.wooden_box) and
            self.check_on(self.tissue_box, self.wooden_box) and
            self.check_on(self.shampoo, self.wooden_box)
        )
