from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 336_place_edible_on_plate_with_recovery(Imagine_Task):
    def load_actors(self):
        # Create the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Create the main objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects
        distractors = ["calculator", "hammer", "toycar", "shoe", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        # Wrong action: Place bottle on plate (needs recovery)
        success = self.pick_and_place(self.bottle, self.plate)
        print("Pick bottle and place on plate (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: Move bottle back to table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover: Move bottle to table:", success)
        if not success:
            return self.info
        
        # Place drinkware (cup_with_handle) on table
        success = self.pick_and_place(self.cup_with_handle, self.table)
        print("Place cup_with_handle on table:", success)
        if not success:
            return self.info
        
        # Place edible items on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries on plate:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.bread, self.plate)
        print("Place bread on plate:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Check if edible items are on the plate
        edible_on_plate = (
            self.check_on(self.french_fries, self.plate) and 
            self.check_on(self.bread, self.plate)
        )
        
        # Check if drinkware are not on the plate
        drinkware_off_plate = (
            not self.check_on(self.bottle, self.plate) and 
            not self.check_on(self.cup_with_handle, self.plate)
        )
        
        return edible_on_plate and drinkware_off_plate
