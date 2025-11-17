from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 448_handle_drinkware_and_dispose_recyclables_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Containers: coaster and dustbin
        - Objects: bottle, mug, screwdriver, pink_block
        - Distractors: alarm-clock, shoe, book, pet-collar, small-speaker
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.mug = self.add_actor("mug", "mug")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.pink_block = self.add_actor("pink_block", "pink_block")

        # Add distractors
        distractors = ["alarm-clock", "shoe", "book", "pet-collar", "small-speaker"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of robot actions:
        1. Place bottle on coaster (wrong action)
        2. Recover by placing bottle into dustbin
        3. Place mug on coaster (correct action)
        4. Place screwdriver into dustbin
        5. Place pink_block into dustbin
        """
        # Step 1: Wrong action - Place bottle on coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Place bottle on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - Place bottle into dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Recover: Place bottle into dustbin:", success)
        if not success:
            return self.info

        # Step 3: Correct action - Place mug on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Place mug on coaster:", success)
        if not success:
            return self.info

        # Step 4: Place screwdriver into dustbin
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("Place screwdriver into dustbin:", success)
        if not success:
            return self.info

        # Step 5: Place pink_block into dustbin
        success = self.pick_and_place(self.pink_block, self.dustbin)
        print("Place pink_block into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Mug is on the coaster
        - Bottle, screwdriver, and pink_block are in the dustbin
        """
        if (
            self.check_on(self.mug, self.coaster) and
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.screwdriver, self.dustbin) and
            self.check_on(self.pink_block, self.dustbin)
        ):
            return True
        return False
