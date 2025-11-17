from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 279_enclosed_storage_and_organizer_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.scanner = self.add_actor("scanner", "scanner")
        self.microphone = self.add_actor("microphone", "microphone")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add distractors
        distractor_list = ['shoe', 'dumbbell', 'pot-with-plant', 'apple', 'hammer']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform to complete the task.
        """
        # Step 1: Place blue_block on fluted_block (wrong action)
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue_block on fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recover blue_block and place it into wooden_box
        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("Recover blue_block to wooden_box:", success)
        if not success:
            return self.info

        # Step 3: Place tissue-box into wooden_box
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("Place tissue-box into wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place yellow_block into wooden_box
        success = self.pick_and_place(self.yellow_block, self.wooden_box)
        print("Place yellow_block into wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place scanner on fluted_block
        success = self.pick_and_place(self.scanner, self.fluted_block)
        print("Place scanner on fluted_block:", success)
        if not success:
            return self.info

        # Step 6: Place microphone on fluted_block
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("Place microphone on fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all objects.
        """
        if (
            self.check_on(self.tissue_box, self.wooden_box) and
            self.check_on(self.blue_block, self.wooden_box) and
            self.check_on(self.yellow_block, self.wooden_box) and
            self.check_on(self.scanner, self.fluted_block) and
            self.check_on(self.microphone, self.fluted_block)
        ):
            return True
        return False
