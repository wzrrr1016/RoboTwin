from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 197_drinkware_and_tools_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.apple = self.add_actor("apple", "apple")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.drill = self.add_actor("drill", "drill")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'alarm-clock', 'toycar', 'book', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of pick-and-place actions for the robot arm.
        Returns early if any action fails.
        """
        # Place apple (perishable food) on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster:", success)
        if not success:
            return self.info

        # Place cup_with_handle (drinkware) on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # Place drill (repair tool) on fluted_block
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Place drill on fluted_block:", success)
        if not success:
            return self.info

        # Place screwdriver (repair tool) on fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver on fluted_block:", success)
        if not success:
            return self.info

        # Place shampoo (personal-care bottle) on fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Place shampoo on fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if all objects are placed correctly according to the task requirements.
        Returns True if all conditions are met, False otherwise.
        """
        # Check if drinkware (cup_with_handle) and perishable food (apple) are on the coaster
        if not (self.check_on(self.cup_with_handle, self.coaster) and self.check_on(self.apple, self.coaster)):
            return False

        # Check if repair tools (drill, screwdriver) and personal-care bottle (shampoo) are on the fluted_block
        if (self.check_on(self.drill, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.shampoo, self.fluted_block)):
            return True

        return False
