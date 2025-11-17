from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 20_heavy_and_fragile_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Containers: wooden_box, fluted_block
        - Objects: dumbbell, drill, screwdriver, apple, bottle
        - Distractors: pot-with-plant, shoe, book, alarm-clock, toycar
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add required objects
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.drill = self.add_actor("drill", "drill")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.apple = self.add_actor("apple", "apple")
        self.bottle = self.add_actor("bottle", "bottle")

        # Add distractors
        distractor_list = ['pot-with-plant', 'shoe', 'book', 'alarm-clock', 'toycar']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions as per the task instructions.
        - Place heavy fitness items and power tools on the fluted_block
        - Place small hand tools, fragile, or perishable items in the wooden_box
        - Correct any wrong placements
        """
        # Step 1: Place dumbbell on fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Place dumbbell on fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Place drill on fluted_block
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Place drill on fluted_block:", success)
        if not success:
            return self.info

        # Step 3: Place screwdriver in wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver in wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Wrong placement of bottle on fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Wrong: Place bottle on fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Recovery: Move bottle to wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Recovery: Place bottle in wooden_box:", success)
        if not success:
            return self.info

        # Step 6: Place apple in wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Place apple in wooden_box:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if all objects are placed in the correct containers as per the task.
        - Dumbbell and drill should be on fluted_block
        - Screwdriver, apple, and bottle should be in wooden_box
        """
        if (self.check_on(self.dumbbell, self.fluted_block) and
            self.check_on(self.drill, self.fluted_block) and
            self.check_on(self.screwdriver, self.wooden_box) and
            self.check_on(self.bottle, self.wooden_box) and
            self.check_on(self.apple, self.wooden_box)):
            return True
        return False
