from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 37_healthy_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.shampoo = self.add_actor("shampoo", "shampoo")

    def play_once(self):
        # Place apple into coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Pick apple into coaster:", success)
        if not success:
            return self.info

        # Place yellow_block into dustbin
        success = self.pick_and_place(self.yellow_block, self.dustbin)
        print("Pick yellow_block into dustbin:", success)
        if not success:
            return self.info

        # Place screwdriver into dustbin
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("Pick screwdriver into dustbin:", success)
        if not success:
            return self.info

        # Place shampoo into dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Pick shampoo into dustbin:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check apple is on coaster
        apple_on_coaster = self.check_on(self.apple, self.coaster)
        # Check yellow_block is on dustbin
        yellow_on_dustbin = self.check_on(self.yellow_block, self.dustbin)
        # Check screwdriver is on dustbin
        screwdriver_on_dustbin = self.check_on(self.screwdriver, self.dustbin)
        # Check shampoo is on dustbin
        shampoo_on_dustbin = self.check_on(self.shampoo, self.dustbin)

        return apple_on_coaster and yellow_on_dustbin and screwdriver_on_dustbin and shampoo_on_dustbin
