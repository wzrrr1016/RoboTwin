from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 50_living_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the dustbin (container)
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Load the living item (pot-with-plant)
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

    def play_once(self):
        # Attempt to pick the pot-with-plant and place it into the dustbin
        success = self.pick_and_place(self.pot_with_plant, self.dustbin)
        print("pick place pot-with-plant:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the pot-with-plant is now on the dustbin
        return self.check_on(self.pot_with_plant, self.dustbin)
