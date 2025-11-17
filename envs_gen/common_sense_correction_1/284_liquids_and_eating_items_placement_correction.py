from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 284_liquids_and_eating_items_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.plate = self.add_actor("plate", "plate")

        # Add objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.bread = self.add_actor("bread", "bread")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors
        distractor_list = ['calculator', 'toycar', 'shoe', 'book', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place knife on coaster
        success = self.pick_and_place(self.knife, self.coaster)
        print("Place knife on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing knife on plate
        success = self.pick_and_place(self.knife, self.plate)
        print("Place knife on plate (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Place bread on plate:", success)
        if not success:
            return self.info

        # Step 5: Place shampoo on coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Place shampoo on coaster:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        # Check if all required objects are in the correct containers
        if (self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.shampoo, self.coaster) and
            self.check_on(self.bread, self.plate) and
            self.check_on(self.knife, self.plate)):
            return True
        return False
