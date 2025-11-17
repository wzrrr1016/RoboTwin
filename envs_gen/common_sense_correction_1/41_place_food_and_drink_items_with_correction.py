from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 41_place_food_and_drink_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.cup = self.add_actor("cup", "cup")
        self.shampoo = self.add_actor("shampoo", "shampoo")

        # Add distractors
        distractor_list = ["calculator", "toycar", "hammer", "book", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place french fries on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french fries:", success)
        if not success:
            return self.info

        # Wrongly place cup on the plate
        success = self.pick_and_place(self.cup, self.plate)
        print("Place cup on plate (wrong):", success)
        if not success:
            return self.info

        # Correct the mistake: move cup to coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster (recovery):", success)
        if not success:
            return self.info

        # Place hamburg on the plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Place hamburg:", success)
        if not success:
            return self.info

        # Place shampoo on the coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Place shampoo:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all correct objects are on the correct containers
        if (
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.hamburg, self.plate) and
            self.check_on(self.cup, self.coaster) and
            self.check_on(self.shampoo, self.coaster)
        ):
            return True
        return False
