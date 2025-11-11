from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 4_toy_and_tool_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.stapler = self.add_actor("stapler", "stapler")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add distractors
        distractor_list = ["apple", "baguette", "jam-jar", "milk-box", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place screwdriver into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver into wooden_box:", success)
        if not success:
            return self.info

        # Step 2: Place stapler onto plate (wrong action)
        success = self.pick_and_place(self.stapler, self.plate)
        print("Place stapler onto plate (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing stapler into wooden_box
        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("Recover: Place stapler into wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place blue_block onto plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Place blue_block onto plate:", success)
        if not success:
            return self.info

        # Step 5: Place yellow_block onto plate
        success = self.pick_and_place(self.yellow_block, self.plate)
        print("Place yellow_block onto plate:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        # Check if blue and yellow blocks are on the plate
        toys_on_plate = (self.check_on(self.blue_block, self.plate) and
                         self.check_on(self.yellow_block, self.plate))
        # Check if screwdriver and stapler are in the wooden_box
        tools_in_wooden_box = (self.check_on(self.screwdriver, self.wooden_box) and
                               self.check_on(self.stapler, self.wooden_box))
        return toys_on_plate and tools_in_wooden_box
