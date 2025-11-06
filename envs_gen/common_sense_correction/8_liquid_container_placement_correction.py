from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 8_liquid_container_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the required containers and object
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.plate = self.add_actor("plate", "plate")
        self.can = self.add_actor("can", "can")

    def play_once(self):
        # Attempt to pick the can and place it into the shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("pick place can:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the can is now on the shoe_box
        return self.check_on(self.can, self.shoe_box)
