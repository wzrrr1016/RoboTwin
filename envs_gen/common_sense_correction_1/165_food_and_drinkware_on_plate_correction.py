from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 165_food_and_drinkware_on_plate_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.book = self.add_actor("book", "book")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors
        distractor_list = ['calculator', 'alarm-clock', 'pot-with-plant', 'dumbbell', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's actions in the environment"""
        # Place edible item (apple) on the plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple on plate:", success)
        if not success:
            return self.info
            
        # Place drinking vessel with handle (cup_with_handle) on the plate
        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Place cup_with_handle on plate:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if edible item and drinking vessel are on the plate
        apple_on_plate = self.check_on(self.apple, self.plate)
        cup_on_plate = self.check_on(self.cup_with_handle, self.plate)
        
        # Check if non-food items are NOT on the plate
        book_off_plate = not self.check_on(self.book, self.plate)
        toycar_off_plate = not self.check_on(self.toycar, self.plate)
        
        # All conditions must be true for success
        return all([apple_on_plate, cup_on_plate, book_off_plate, toycar_off_plate])
