from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_placement_mistake_correction(Imagine_Task):
    def load_actors(self):
        # Load the plate and wooden box as containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load the healthy and non-healthy items
        self.healthy_items = ["apple", "fork"]
        self.non_healthy_items = ["hamburg", "pot-with-plant", "knife"]

        # Load each item
        for item in self.healthy_items + self.non_healthy_items:
            self.add_actor(item, item)

    def play_once(self):
        # Define the containers for healthy and non-healthy items
        healthy_container = self.plate
        non_healthy_container = self.wooden_box

        # Pick and place healthy items into the plate
        for item in self.healthy_items:
            success = self.pick_and_place(item, healthy_container)
            print(f"Pick and place {item}:", success)
            if not success:
                return self.info

        # Pick and place non-healthy items into the wooden box
        for item in self.non_healthy_items:
            success = self.pick_and_place(item, non_healthy_container)
            print(f"Pick and place {item}:", success)
            if not success:
                return self.info

        return self.info

    def check_success(self):
        # Check if all healthy items are on the plate and all non-healthy items are in the wooden box
        for item in self.healthy_items:
            if not self.check_on(item, self.plate):
                return False
        for item in self.non_healthy_items:
            if not self.check_on(item, self.wooden_box):
                return False

        return True

# Example usage:
# task = PlaceItemsTask()
# task.load_actors()
# task.play_once()
# success = task.check_success()
# print("Task completed successfully:", success)
