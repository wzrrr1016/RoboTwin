from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 144_place_food_and_household_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.scanner = self.add_actor("scanner", "scanner")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        
        # Add distractors
        distractor_list = ["toycar", "red_block", "green_block", "blue_block", "yellow_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick tissue-box and place it into shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("Place tissue-box into shoe_box:", success)
        if not success:
            return self.info

        # 2. Pick bread and place it into shoe_box (wrong)
        success = self.pick_and_place(self.bread, self.shoe_box)
        print("Place bread into shoe_box (wrong):", success)
        if not success:
            return self.info

        # 3. Pick bread from shoe_box and place it into plate (recovery)
        success = self.pick_and_place(self.bread, self.plate)
        print("Recover bread to plate:", success)
        if not success:
            return self.info

        # 4. Pick french_fries and place it into plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries into plate:", success)
        if not success:
            return self.info

        # 5. Pick scanner and place it into shoe_box
        success = self.pick_and_place(self.scanner, self.shoe_box)
        print("Place scanner into shoe_box:", success)
        if not success:
            return self.info

        # 6. Pick cup_with_handle and place it into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Place cup_with_handle into shoe_box:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        # Check if edible perishable foods are on the plate
        bread_on_plate = self.check_on(self.bread, self.plate)
        french_fries_on_plate = self.check_on(self.french_fries, self.plate)
        
        # Check if non-food household items are in the shoe_box
        tissue_in_shoe_box = self.check_on(self.tissue_box, self.shoe_box)
        scanner_in_shoe_box = self.check_on(self.scanner, self.shoe_box)
        cup_in_shoe_box = self.check_on(self.cup_with_handle, self.shoe_box)
        
        # Ensure bread is not in shoe_box (recovery was successful)
        bread_not_in_shoe_box = not self.check_on(self.bread, self.shoe_box)
        
        return (bread_on_plate and french_fries_on_plate and 
                tissue_in_shoe_box and scanner_in_shoe_box and 
                cup_in_shoe_box and bread_not_in_shoe_box)
