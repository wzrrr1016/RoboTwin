from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class container_usage_correction(Imagine_Task):
    def load_actors(self):
        # Load the actors into the environment
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.stapler = self.add_actor("stapler", "stapler")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.toy_car = self.add_actor("toycar", "toycar")

    def play_once(self):
        # Pick up the stapler and place it in the shoe_box
        success = self.pick_and_place(self.stapler, self.shoe_box)
        print("Pick and place stapler:", success)
        if not success:
            return self.info

        # Attempt to pick up the tissue-box and place it in the dustbin (should fail)
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Pick and place tissue-box (should fail):", success)
        if not success:
            # If the placement fails, pick up the tissue-box from the dustbin and place it in the shoe_box
            success = self.pick_and_place(self.tissue_box, self.dustbin)
            print("Pick and place tissue-box (recovery):", success)
            if not success:
                return self.info

        # Pick up the toy_car and place it in the dustbin
        success = self.pick_and_place(self.toy_car, self.dustbin)
        print("Pick and place toy_car:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if the stapler is on the shoe_box and the toy_car is on the dustbin
        stapler_on_shoe_box = self.check_on(self.stapler, self.shoe_box)
        toy_car_in_dustbin = self.check_on(self.toy_car, self.dustbin)
        return stapler_on_shoe_box and toy_car_in_dustbin

# Example usage:
# task = StoreSuppliesTask()
# task.load_actors()
# task.play_once()
# success = task.check_success()
# print("Task completed successfully:", success)
