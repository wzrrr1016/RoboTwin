from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 469_place_blocks_and_eatware_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers, target objects, and distractors.
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block_0")
        self.coaster = self.add_actor("coaster", "coaster_0")

        # Add target objects
        self.orange_block = self.add_actor("orange_block", "orange_block_0")
        self.green_block = self.add_actor("green_block", "green_block_0")
        self.pink_block = self.add_actor("pink_block", "pink_block_0")
        self.apple = self.add_actor("apple", "apple_0")
        self.fork = self.add_actor("fork", "fork_0")

        # Add distractors
        distractor_list = ["calculator", "stapler", "pot-with-plant", "alarm-clock", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        This includes placing blocks in the fluted_block and edible/utensil items on the coaster.
        """
        # Step 1: Place orange_block into fluted_block
        success = self.pick_and_place(self.orange_block, self.fluted_block)
        print("Place orange_block:", success)
        if not success:
            return self.info

        # Step 2: Place apple into fluted_block (wrong action)
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Wrong: apple to fluted_block:", success)
        if not success:
            return self.info

        # Step 3: Recover by placing apple onto coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Recover: apple to coaster:", success)
        if not success:
            return self.info

        # Step 4: Place green_block into fluted_block
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block:", success)
        if not success:
            return self.info

        # Step 5: Place pink_block into fluted_block
        success = self.pick_and_place(self.pink_block, self.fluted_block)
        print("Place pink_block:", success)
        if not success:
            return self.info

        # Step 6: Place fork onto coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("Place fork:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        This includes verifying the final positions of all relevant objects.
        """
        # Check if all blocks are in the fluted_block
        blocks_in_fluted = (
            self.check_on(self.orange_block, self.fluted_block) and
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.pink_block, self.fluted_block)
        )

        # Check if apple and fork are on the coaster
        items_on_coaster = (
            self.check_on(self.apple, self.coaster) and
            self.check_on(self.fork, self.coaster)
        )

        # Return True only if all conditions are met
        return blocks_in_fluted and items_on_coaster
