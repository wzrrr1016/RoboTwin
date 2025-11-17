from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 60_perishable_food_grouping_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Containers: fluted_block
        - Objects: bread, small-speaker, apple, hamburg
        - Distractors: shoe, book, pot-with-plant, dumbbell, stapler
        """
        # Add the organizer surface (fluted_block)
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the food items and electronic device
        self.bread = self.add_actor("bread", "bread")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")

        # Add distractor objects
        distractor_list = ["shoe", "book", "pot-with-plant", "dumbbell", "stapler"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm:
        1. Place bread into fluted_block
        2. Place small-speaker into fluted_block (wrong action)
        3. Recover by placing small-speaker on the table
        4. Place apple into fluted_block
        5. Place hamburg into fluted_block
        """
        # Place bread into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread:", success)
        if not success:
            return self.info

        # Wrongly place small-speaker into fluted_block
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Wrongly place small-speaker:", success)
        if not success:
            return self.info

        # Recover: place small-speaker on the table
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Recover small-speaker:", success)
        if not success:
            return self.info

        # Place apple into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info

        # Place hamburg into fluted_block
        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("Place hamburg:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - All perishable, ready-to-eat foods (bread, apple, hamburg) are on fluted_block
        - Electronic device (small-speaker) is on the table (not on fluted_block)
        """
        if (
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.hamburg, self.fluted_block) and
            self.check_on(self.small_speaker, self.table)
        ):
            return True
        return False
