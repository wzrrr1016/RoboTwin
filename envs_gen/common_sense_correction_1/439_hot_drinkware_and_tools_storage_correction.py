from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 439_hot_drinkware_and_tools_storage_correction(Imagine_Task):
    def load_actors(self):
        # Load the container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Load the objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Load distractors
        distractor_list = ["calculator", "toycar", "book", "alarm-clock", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick screwdriver and place it onto shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Pick screwdriver:", success)
        if not success:
            return self.info

        # 2. Pick mug and place it into shoe_box
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Pick mug:", success)
        if not success:
            return self.info

        # 3. Pick cup_without_handle and place it into shoe_box (wrong)
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("Pick cup_without_handle (wrong):", success)
        if not success:
            return self.info

        # 4. Pick cup_without_handle from shoe_box and place it onto shoe_box (recovery)
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("Recover cup_without_handle:", success)
        if not success:
            return self.info

        # 5. Pick cup_with_handle and place it into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Pick cup_with_handle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all objects are correctly placed
        if (
            self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.mug, self.shoe_box) and
            self.check_on(self.cup_with_handle, self.shoe_box) and
            self.check_on(self.cup_without_handle, self.shoe_box)
        ):
            return True
        return False
