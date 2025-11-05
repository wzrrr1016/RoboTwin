from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_and_tableware_placement_12(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Load healthy foods
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")

        # Load tableware
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")

    def play_once(self):
        # Place apple on the plate
        success = self.pick_and_place(self.apple, self.plate)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Place french fries on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("pick place french fries:", success)
        if not success:
            return self.info

        # Place fork in the dustbin
        success = self.pick_and_place(self.fork, self.dustbin)
        print("pick place fork:", success)
        if not success:
            return self.info

        # Place knife in the dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("pick place knife:", success)
        if not success:
            return self.info

        # Place cup_without_handle in the dustbin
        success = self.pick_and_place(self.cup_without_handle, self.dustbin)
        print("pick place cup_without_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if healthy foods are on the plate
        if self.check_on(self.apple, self.plate) and self.check_on(self.french_fries, self.plate):
            # Check if tableware is in the dustbin
            if self.check_on(self.fork, self.dustbin) and self.check_on(self.knife, self.dustbin) and self.check_on(self.cup_without_handle, self.dustbin):
                return True
        return False
