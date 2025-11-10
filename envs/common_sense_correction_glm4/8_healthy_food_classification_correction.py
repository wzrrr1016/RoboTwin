from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_classification_correction(Imagine_Task):
    def load_actors(self):
        # Load the plate and tray actors
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        
        # Load the food items (healthy)
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Load the non-food items
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

    def play_once(self):
        # Pick the apple and place it into the plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Pick and place apple:", success)
        if not success:
            return self.info
        
        # Attempt to pick the dumbbell and place it into the tray (should fail)
        success = self.pick_and_place(self.dumbbell, self.tray)
        print("Pick and place dumbbell (should fail):", success)
        if not success:
            return self.info
        
        # Pick the dumbbell from the tray and place it into the plate (recovery)
        success = self.pick_and_place(self.dumbbell, self.plate)
        print("Pick and place dumbbell (recovery):", success)
        if not success:
            return self.info
        
        # Pick the hamburger and place it into the tray
        success = self.pick_and_place(self.hamburg, self.tray)
        print("Pick and place hamburger:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the apple is on the plate and the hamburger is on the tray
        apple_on_plate = self.check_on(self.apple, self.plate)
        hamburg_on_tray = self.check_on(self.hamburg, self.tray)
        
        # Check if the dumbbell is on the plate (it should be there after recovery)
        dumbbell_on_plate = self.check_on(self.dumbbell, self.plate)
        
        # Return True if all conditions are met
        return apple_on_plate and hamburg_on_tray and dumbbell_on_plate

# Example usage:
# task = PlaceFoodTask()
# task.load_actors()
# task.play_once()
# success = task.check_success()
# print("Task successful:", success)
