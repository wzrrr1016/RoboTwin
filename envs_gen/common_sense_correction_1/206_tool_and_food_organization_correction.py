from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 206_tool_and_food_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers, target objects, and distractors.
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add target objects
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.cup = self.add_actor("cup", "cup")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractors
        distractor_list = ['toycar', 'pot-with-plant', 'book', 'shoe', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        This includes both correct and recovery actions as specified in the task.
        """
        # Step 1: Wrong placement of hamburg into wooden_box
        success = self.pick_and_place(self.hamburg, self.wooden_box)
        print("Pick hamburg into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - move hamburg to fluted_block
        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("Recover hamburg to fluted_block:", success)
        if not success:
            return self.info

        # Step 3: Place french_fries on fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french_fries on fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Place cup on fluted_block
        success = self.pick_and_place(self.cup, self.fluted_block)
        print("Place cup on fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place screwdriver in wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver in wooden_box:", success)
        if not success:
            return self.info

        # Step 6: Place dumbbell in wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Place dumbbell in wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The success condition is:
        - Tools and heavy exercise items in wooden_box
        - Edible items and drinkware on fluted_block
        """
        if (
            self.check_on(self.screwdriver, self.wooden_box) and
            self.check_on(self.dumbbell, self.wooden_box) and
            self.check_on(self.hamburg, self.fluted_block) and
            self.check_on(self.french_fries, self.fluted_block) and
            self.check_on(self.cup, self.fluted_block)
        ):
            return True
        return False
