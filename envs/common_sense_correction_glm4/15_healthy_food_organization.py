from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_organization(Imagine_Task):
    def load_actors(self):
        # Load the containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load the objects
        self.apple = self.add_actor("apple", "apple")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bottle = self.add_actor("bottle", "bottle")
        self.hamburg = self.add_actor("hamburg", "hamburg")

    def play_once(self):
        # Define healthy and unhealthy items
        healthy_items = [self.apple, self.tissue_box, self.bottle]
        unhealthy_items = [self.dumbbell, self.hamburg]

        # Organize healthy items into the fluted_block
        for item in healthy_items:
            success = self.pick_and_place(item, self.fluted_block)
            print(f"Pick and place {item.name}:", success)
            if not success:
                return self.info

        # Organize unhealthy items into the wooden_box
        for item in unhealthy_items:
            success = self.pick_and_place(item, self.wooden_box)
            print(f"Pick and place {item.name}:", success)
            if not success:
                return self.info

    def check_success(self):
        # Check if all healthy items are on the fluted_block and all unhealthy items are on the wooden_box
        for item in self.wooden_box.get_functional_points():
            if item.return_type == "pose" and item.p[0] > 0.5:  # Assuming the wooden_box is placed at x > 0.5
                return False

        for item in self.fluted_block.get_functional_points():
            if item.return_type == "pose" and item.p[0] < -0.5:  # Assuming the fluted_block is placed at x < -0.5
                return False

        return True

# Example usage:
# task = OrganizeItemsTask()
# task.load_actors()
# task.play_once()
# if task.check_success():
#     print("Task completed successfully.")
# else:
#     print("Task failed.")
