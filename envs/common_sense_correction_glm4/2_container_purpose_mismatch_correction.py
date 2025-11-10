from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class container_purpose_mismatch_correction(Imagine_Task):
    def load_actors(self):
        # Load the containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Load the office supplies
        self.stapler = self.add_actor("stapler", "stapler")
        self.can = self.add_actor("can", "can")

        # Load the non-office items
        self.mouse = self.add_actor("mouse", "mouse")
        self.french_fries = self.add_actor("french_fries", "french_fries")

    def play_once(self):
        # Pick up the stapler and place it in the wooden box
        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("Pick and place stapler:", success)

        # Pick up the can and place it in the wooden box (wrong action)
        success = self.pick_and_place(self.can, self.wooden_box)
        print("Pick and place can (wrong):", success)

        # Pick up the can from the wooden box and place it in the shoe box (recovery)
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Pick and place can (recovery):", success)

        # Pick up the mouse and place it in the wooden box
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Pick and place mouse:", success)

        # Pick up the french fries and place it in the shoe box
        success = self.pick_and_place(self.french_fries, self.shoe_box)
        print("Pick and place french fries:", success)

        return success

    def check_success(self):
        # Check if the stapler is on the wooden box
        if not self.check_on(self.stapler, self.wooden_box):
            return False

        # Check if the can is on the shoe box
        if not self.check_on(self.can, self.shoe_box):
            return False

        # Check if the mouse is on the wooden box
        if not self.check_on(self.mouse, self.wooden_box):
            return False

        # Check if the french fries are on the shoe box
        if not self.check_on(self.french_fries, self.shoe_box):
            return False

        return True

# Example usage:
# task = StoreSuppliesTask()
# task.load_actors()
# success = task.play_once()
# if success:
#     print("Task completed successfully.")
# else:
#     print("Task failed.")
