from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 201_dispose_single_use_and_store_reusables_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractors
        distractor_list = ["chips-tub", "alarm-clock", "small-speaker", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place tissue-box into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Place tissue-box into dustbin:", success)
        if not success:
            return self.info

        # Step 2: Place mug into shoe_box
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Place mug into shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Place cup_with_handle into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Place cup_with_handle into shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Place toycar into dustbin (wrong action)
        success = self.pick_and_place(self.toycar, self.dustbin)
        print("Place toycar into dustbin (wrong):", success)
        if not success:
            return self.info

        # Step 5: Recover toycar into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Recover toycar into shoe_box:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        # Check if all required objects are in the correct containers
        if (
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.mug, self.shoe_box) and
            self.check_on(self.cup_with_handle, self.shoe_box) and
            self.check_on(self.toycar, self.shoe_box)
        ):
            return True
        return False
