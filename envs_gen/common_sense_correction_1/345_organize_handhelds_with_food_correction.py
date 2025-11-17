from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 345_organize_handhelds_with_food_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and distractors) into the simulation environment.
        """
        # Add the container (fluted_block) to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the required objects to the environment
        self.markpen = self.add_actor("markpen", "markpen")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.mug = self.add_actor("mug", "mug")
        self.apple = self.add_actor("apple", "apple")

        # Add distractor objects to the environment
        distractors = ["pot-with-plant", "alarm-clock", "small-speaker", "book", "shoe"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        """
        # Step 1: Place the markpen into the fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Place markpen:", success)
        if not success:
            return self.info

        # Step 2: Place the screwdriver into the fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        # Step 3: Place the mug into the fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug:", success)
        if not success:
            return self.info

        # Step 4: Place the apple into the fluted_block (wrong action)
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple (wrong):", success)
        if not success:
            return self.info

        # Step 5: Recover by placing the apple into the mug
        success = self.pick_and_place(self.apple, self.mug)
        print("Recover apple to mug:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully based on the defined conditions.
        """
        # Check if all handheld items are on the fluted_block
        markpen_on = self.check_on(self.markpen, self.fluted_block)
        screwdriver_on = self.check_on(self.screwdriver, self.fluted_block)
        mug_on = self.check_on(self.mug, self.fluted_block)

        # Check if the apple is on the mug (perishable food with drinkware)
        apple_on_mug = self.check_on(self.apple, self.mug)

        # Return True only if all conditions are met
        return markpen_on and screwdriver_on and mug_on and apple_on_mug
