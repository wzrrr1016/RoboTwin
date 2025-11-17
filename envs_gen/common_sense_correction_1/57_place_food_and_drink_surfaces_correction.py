from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 57_place_food_and_drink_surfaces_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add required objects
        self.bread = self.add_actor("bread", "bread")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractors
        distractor_list = ["calculator", "alarm-clock", "pot-with-plant", "toycar", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place edible items and utensils on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Bread to plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.fork, self.plate)
        print("Fork to plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.knife, self.plate)
        print("Knife to plate:", success)
        if not success:
            return self.info
            
        # Wrong placement (bottle on plate)
        success = self.pick_and_place(self.bottle, self.plate)
        print("Bottle to plate (wrong):", success)
        if not success:
            return self.info
            
        # Recovery (bottle to coaster)
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Bottle to coaster:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all items are in their correct locations
        return (
            self.check_on(self.bread, self.plate) and
            self.check_on(self.fork, self.plate) and
            self.check_on(self.knife, self.plate) and
            self.check_on(self.bottle, self.coaster)
        )
