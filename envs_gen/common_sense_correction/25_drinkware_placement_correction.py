from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 25_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add the drinkware objects (cups) and apple
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.apple = self.add_actor("apple", "apple")
        
        # Add distractor objects
        distractor_list = ['calculator', 'screwdriver', 'toycar', 'pot-with-plant', 'alarm-clock', 'dumbbell']
        self.add_distractors(distractor_list)
        
        # Finalize scene setup
        self.check_scene()

    def play_once(self):
        # Step 1: Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        # Step 2: Place cup_without_handle on coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Place cup_without_handle:", success)
        if not success:
            return self.info

        # Step 3: Place apple on coaster (wrong action)
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover by placing apple back on table
        success = self.pick_and_place(self.apple, self.table)
        print("Recover apple to table:", success)
        if not success:
            return self.info

        # Mark task completion
        self.add_end()
        return self.info

    def check_success(self):
        # Success condition: both cups on coaster, apple not on coaster
        if (self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.cup_without_handle, self.coaster) and
            not self.check_on(self.apple, self.coaster)):
            return True
        return False
