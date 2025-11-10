from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load the actors into the environment
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.apple = self.add_actor("apple", "apple")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.apple_sauce = self.add_actor("bottle", "apple_sauce")  # Assuming apple_sauce is a bottle type

    def play_once(self):
        # Define the actions to be performed
        actions = [
            ("pick", self.apple, self.plate),
            ("pick", self.fork, self.wooden_box),
            ("pick", self.knife, self.wooden_box),
            ("pick", self.apple_sauce, self.wooden_box),
            ("pick", self.fork, self.wooden_box),  # Pick fork from wooden_box
            ("place", self.fork, self.plate),     # Place fork into plate
        ]

        for action in actions:
            action_type, object, container = action
            if action_type == "pick":
                success = self.pick_and_place(object, container)
                print(f"Pick {object.get_name()}:", success)
                if not success:
                    return self.info
            elif action_type == "place":
                success = self.pick_and_place(object, container)
                print(f"Place {object.get_name()} in {container.get_name()}:", success)
                if not success:
                    return self.info

    def check_success(self):
        # Check if the task was completed successfully
        # The apple should be on the plate, and the fork, knife, and apple_sauce should be in the wooden_box
        plate_items = [self.check_on(item, self.plate) for item in [self.apple, self.fork, self.knife, self.apple_sauce]]
        wooden_box_items = [self.check_on(item, self.wooden_box) for item in [self.fork, self.knife, self.apple_sauce]]

        return all(plate_items) and all(wooden_box_items)

# Example usage:
# task = PlaceFoodTask()
# task.load_actors()
# task.play_once()
# success = task.check_success()
# print("Task completed successfully:", success)
