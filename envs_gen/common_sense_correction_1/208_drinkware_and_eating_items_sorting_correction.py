from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 208_drinkware_and_eating_items_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add required containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.plate = self.add_actor("plate", "plate")
        
        # Add required objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractors = ["calculator", "toycar", "screwdriver", "alarm-clock", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        # Place french fries on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french fries on plate:", success)
        if not success:
            return self.info

        # Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info

        # Wrong placement: Place fork on coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("Wrong: Place fork on coaster:", success)
        if not success:
            return self.info

        # Recovery: Move fork to plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Recover: Place fork on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if drinkware is on coaster
        cup_on_coaster = self.check_on(self.cup_with_handle, self.coaster)
        
        # Check if edible items are on plate
        fries_on_plate = self.check_on(self.french_fries, self.plate)
        
        # Check if eating utensils are on plate
        fork_on_plate = self.check_on(self.fork, self.plate)
        
        # All conditions must be satisfied for success
        return cup_on_coaster and fries_on_plate and fork_on_plate
