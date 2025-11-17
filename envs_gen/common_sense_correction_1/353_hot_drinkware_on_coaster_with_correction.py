from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 353_hot_drinkware_on_coaster_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        # Add the relevant objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.apple = self.add_actor("apple", "apple")
        # Add distractors
        distractors = ["calculator", "battery", "toycar", "book", "small-speaker"]
        self.add_distractors(distractors)

    def play_once(self):
        # Step 1: Pick mug and place on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Place mug on coaster:", success)
        if not success:
            return self.info

        # Step 2: Pick apple and place on coaster (wrong action)
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick apple from coaster and place into cup_without_handle (recovery)
        success = self.pick_and_place(self.apple, self.cup_without_handle)
        print("Move apple to cup_without_handle:", success)
        if not success:
            return self.info

        # Step 4: Pick cup_with_handle and place on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if mug is on coaster
        mug_on = self.check_on(self.mug, self.coaster)
        # Check if cup_with_handle is on coaster
        cup_with_handle_on = self.check_on(self.cup_with_handle, self.coaster)
        # Check if apple is not on coaster
        apple_not_on = not self.check_on(self.apple, self.coaster)
        # Check if cup_without_handle is not on coaster
        cup_without_handle_not_on = not self.check_on(self.cup_without_handle, self.coaster)

        return mug_on and cup_with_handle_on and apple_not_on and cup_without_handle_not_on
