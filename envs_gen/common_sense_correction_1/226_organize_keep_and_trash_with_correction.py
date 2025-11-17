from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 226_organize_keep_and_trash_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: fluted_block (organizer), dustbin
        - Objects: apple, french_fries, bottle, toycar
        - Distractors: calculator, screwdriver, alarm-clock, dumbbell, book
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add required objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bottle = self.add_actor("bottle", "bottle")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractors
        distractor_list = ["calculator", "screwdriver", "alarm-clock", "dumbbell", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions to complete the task:
        1. Pick apple and place it into fluted_block
        2. Pick toycar and place it into fluted_block
        3. Pick bottle and place it into fluted_block (wrong)
        4. Pick bottle from fluted_block and place it into dustbin (recovery)
        5. Pick french_fries and place it into fluted_block
        """
        # Step 1: Place apple into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info

        # Step 2: Place toycar into fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

        # Step 3: Place bottle into fluted_block (wrong)
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover bottle to dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Recover bottle:", success)
        if not success:
            return self.info

        # Step 5: Place french_fries into fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french_fries:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Apple, toycar, and french_fries are in fluted_block
        - Bottle is in dustbin
        """
        if (
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.french_fries, self.fluted_block) and
            self.check_on(self.bottle, self.dustbin)
        ):
            return True
        return False
