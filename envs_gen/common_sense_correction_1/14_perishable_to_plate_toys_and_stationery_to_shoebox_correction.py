from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 14_perishable_to_plate_toys_and_stationery_to_shoebox_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.markpen = self.add_actor("markpen", "markpen")

        # Add distractors
        distractor_list = ["drill", "hammer", "dumbbell", "pot-with-plant", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: apple to shoe_box
        self.pick_and_place(self.apple, self.shoe_box)

        # Recovery: apple to plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Recovery apple to plate:", success)
        if not success:
            return self.info

        # Correct actions
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Place yellow_block into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("Place purple_block into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Place markpen into shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        if (self.check_on(self.apple, self.plate) and
            self.check_on(self.yellow_block, self.shoe_box) and
            self.check_on(self.purple_block, self.shoe_box) and
            self.check_on(self.markpen, self.shoe_box)):
            return True
        return False
