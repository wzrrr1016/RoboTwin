from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 97_drinkware_and_tools_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add required objects to the environment
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractor objects to the environment
        distractor_list = ["toycar", "book", "alarm-clock", "small-speaker", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place hammer into shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Place hammer:", success)
        if not success:
            return self.info

        # Step 2: Place mug into shoe_box (wrong action)
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Place mug into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing mug onto coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Recover mug to coaster:", success)
        if not success:
            return self.info

        # Step 4: Place cup_without_handle onto coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Place cup without handle:", success)
        if not success:
            return self.info

        # Step 5: Place drill into shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Place drill:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify final state: 
        # - Drinkware (mug and cup_without_handle) on coaster
        # - Tools (hammer and drill) in shoe_box
        if (self.check_on(self.mug, self.coaster) and
            self.check_on(self.cup_without_handle, self.coaster) and
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.drill, self.shoe_box)):
            return True
        return False
