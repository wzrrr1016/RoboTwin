from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 198_place_edibles_and_drinkware_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.book = self.add_actor("book", "book")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "battery", "dumbbell", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place edible food and drink containers on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries on plate:", success)
        if not success:
            return self.info
        
        # Wrongly place book on plate (recovery step)
        success = self.pick_and_place(self.book, self.plate)
        print("Wrongly place book on plate:", success)
        if not success:
            return self.info
        
        # Correct by placing book into dustbin
        success = self.pick_and_place(self.book, self.dustbin)
        print("Place book into dustbin:", success)
        if not success:
            return self.info
        
        # Place bottle on plate
        success = self.pick_and_place(self.bottle, self.plate)
        print("Place bottle on plate:", success)
        if not success:
            return self.info
        
        # Place cup_without_handle on plate
        success = self.pick_and_place(self.cup_without_handle, self.plate)
        print("Place cup_without_handle on plate:", success)
        if not success:
            return self.info
        
        # Place toycar into dustbin
        success = self.pick_and_place(self.toycar, self.dustbin)
        print("Place toycar into dustbin:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Check if edible foods and drink containers are on the plate
        on_plate = (
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.bottle, self.plate) and
            self.check_on(self.cup_without_handle, self.plate)
        )
        
        # Check if non-food items and toys are in the dustbin
        in_dustbin = (
            self.check_on(self.book, self.dustbin) and
            self.check_on(self.toycar, self.dustbin)
        )
        
        return on_plate and in_dustbin
