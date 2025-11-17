from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 401_drinkware_and_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractors
        distractor_list = ['calculator', 'battery', 'book', 'shoe', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick mug and place on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Pick mug and place on coaster:", success)
        if not success:
            return self.info

        # 2. Pick french_fries and place on coaster (wrong)
        success = self.pick_and_place(self.french_fries, self.coaster)
        print("Pick french_fries and place on coaster (wrong):", success)
        if not success:
            return self.info

        # 3. Pick french_fries from coaster and place on plate (recovery)
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Pick french_fries from coaster and place on plate:", success)
        if not success:
            return self.info

        # 4. Pick cup_with_handle and place on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Pick cup_with_handle and place on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all task requirements are met
        if (self.check_on(self.mug, self.coaster) and
            self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.french_fries, self.plate)):
            return True
        return False
