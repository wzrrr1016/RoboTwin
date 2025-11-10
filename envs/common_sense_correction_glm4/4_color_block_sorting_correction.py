from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load the plate and coaster as containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")

        # Load the color blocks as objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        # ... Load other blocks as needed

    def play_once(self):
        # Define the order of actions
        actions = [
            ("pick", self.red_block, self.plate),
            ("pick", self.microphone, self.coaster),  # This will be wrong
            ("pick", self.microphone, self.plate),    # Recovery action
            ("pick", self.green_block, self.coaster)
        ]

        for action in actions:
            action_type, object, container = action
            if action_type == "pick":
                success = self.pick_and_place(object, container)
                print(f"Pick and place {object} into {container}: {success}")
                if not success:
                    return self.info

    def check_success(self):
        # Check if the primary color block is on the plate
        if self.check_on(self.red_block, self.plate):
            # Check if the secondary color block is on the coaster
            if self.check_on(self.green_block, self.coaster):
                return True
        return False

# Example usage:
# task = SortBlocksTask()
# task.load_actors()
# task.play_once()
# success = task.check_success()
# print("Task successful:", success)
