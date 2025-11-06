from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 32_dangerous_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.knife = self.add_actor("knife", "knife")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

    def play_once(self):
        # Place knife into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("pick place knife:", success)
        if not success:
            return self.info

        # Place screwdriver into shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("pick place screwdriver:", success)
        if not success:
            return self.info

        # Place purple_block into shoe_box
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("pick place purple_block:", success)
        if not success:
            return self.info

        # Place yellow_block into shoe_box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if knife is in wooden_box
        knife_in_wooden = self.check_on(self.knife, self.wooden_box)
        # Check if screwdriver is in shoe_box
        screwdriver_in_shoe = self.check_on(self.screwdriver, self.shoe_box)
        # Check if purple_block is in shoe_box
        purple_in_shoe = self.check_on(self.purple_block, self.shoe_box)
        # Check if yellow_block is in shoe_box
        yellow_in_shoe = self.check_on(self.yellow_block, self.shoe_box)

        return knife_in_wooden and screwdriver_in_shoe and purple_in_shoe and yellow_in_shoe
