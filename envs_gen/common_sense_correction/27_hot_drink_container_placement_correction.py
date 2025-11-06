from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 27_hot_drink_container_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        # Load the cups (one for hot drinks, one not suitable)
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        # Load other objects in the scene
        self.microphone = self.add_actor("microphone", "microphone")
        self.mouse = self.add_actor("mouse", "mouse")
        self.shampoo = self.add_actor("shampoo", "shampoo")

    def play_once(self):
        # First attempt: place the wrong cup into the coaster (wrong action)
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("pick place cup_without_handle into coaster:", success)
        if not success:
            return self.info

        # Recovery: pick the wrong cup from the coaster and place it on the table
        success = self.pick_and_place(self.cup_without_handle, self.table)
        print("pick place cup_without_handle on table:", success)
        if not success:
            return self.info

        # Correct action: place the cup_with_handle into the coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("pick place cup_with_handle into coaster:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the correct cup is on the coaster
        return self.check_on(self.cup_with_handle, self.coaster)
