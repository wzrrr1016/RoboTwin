from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 15_plate_for_food_and_kitchen_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the simulation environment"""
        # Create containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create target objects
        self.apple = self.add_actor("apple", "apple")
        self.teanet = self.add_actor("teanet", "teanet")
        self.shoe = self.add_actor("shoe", "shoe")
        self.book = self.add_actor("book", "book")
        
        # Add distractor objects
        distractor_list = ["calculator", "screwdriver", "toycar", "alarm-clock", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of pick-and-place actions"""
        # Place edible/kitchen items on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple on plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.teanet, self.plate)
        print("Place teanet on plate:", success)
        if not success:
            return self.info
            
        # Place wearable/reading items in shoe box
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Place shoe in shoe_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Place book in shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if all objects are placed correctly"""
        return (
            self.check_on(self.apple, self.plate) and
            self.check_on(self.teanet, self.plate) and
            self.check_on(self.shoe, self.shoe_box) and
            self.check_on(self.book, self.shoe_box)
        )
