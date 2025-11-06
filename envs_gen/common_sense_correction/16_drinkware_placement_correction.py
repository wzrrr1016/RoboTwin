from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 16_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        # Add the drinkware item (cup_without_handle)
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        # Add other objects (not used in this task, but included as per the scene)
        self.apple = self.add_actor("apple", "apple")
        self.scanner = self.add_actor("scanner", "scanner")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

    def play_once(self):
        # Attempt to pick up the cup_without_handle and place it into the coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("pick place cup_without_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the cup_without_handle is on the coaster
        return self.check_on(self.cup_without_handle, self.coaster)
