from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 48_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        # Add the drinkware items
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        # Add other objects (not required for the task)
        self.drill = self.add_actor("drill", "drill")
        self.scanner = self.add_actor("scanner", "scanner")
        self.mouse = self.add_actor("mouse", "mouse")

    def play_once(self):
        # Pick and place the first cup
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Pick and place cup_without_handle:", success)
        if not success:
            return self.info

        # Pick and place the second cup
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Pick and place cup_with_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if both cups are on the coaster
        if self.check_on(self.cup_without_handle, self.coaster) and self.check_on(self.cup_with_handle, self.coaster):
            return True
        return False
