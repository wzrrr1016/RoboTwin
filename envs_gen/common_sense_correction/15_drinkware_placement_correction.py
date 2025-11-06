from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 15_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the coaster (container)
        self.coaster = self.add_actor("coaster", "coaster")
        # Load the shampoo (wrong item)
        self.shampoo = self.add_actor("shampoo", "shampoo")
        # Load the cup_with_handle (correct drinkware)
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        # Load other objects (not relevant to the task)
        self.red_block = self.add_actor("red_block", "red_block")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

    def play_once(self):
        # Step 1: Attempt to place shampoo into coaster (wrong action)
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("pick place shampoo:", success)
        if not success:
            # Step 2: Recovery: pick shampoo from coaster and place on table
            success = self.pick_and_place(self.shampoo, self.coaster)
            print("pick place shampoo from coaster:", success)
            if not success:
                return self.info
            success = self.pick_and_place(self.shampoo, self.table)
            print("place shampoo on table:", success)
            if not success:
                return self.info

        # Step 3: Correct action: place cup_with_handle into coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the cup_with_handle is on the coaster
        return self.check_on(self.cup_with_handle, self.coaster)
