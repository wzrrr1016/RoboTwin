from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class food_sorting_and_correction_27(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.knife = self.add_actor("knife", "knife")
        self.hamburg = self.add_actor("hamburg", "hamburg")

    def play_once(self):
        # Place non-food items into dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("pick place knife:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.orange_block, self.dustbin)
        print("pick place orange_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.pot_with_plant, self.dustbin)
        print("pick place pot_with_plant:", success)
        if not success:
            return self.info

        # Place food item into plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("pick place hamburg:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all non-food items are in dustbin and food item is in plate
        return (
            self.check_on(self.knife, self.dustbin) and
            self.check_on(self.orange_block, self.dustbin) and
            self.check_on(self.pot_with_plant, self.dustbin) and
            self.check_on(self.hamburg, self.plate)
        )
