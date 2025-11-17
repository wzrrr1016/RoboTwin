from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 312_hot_beverage_and_utensil_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Add required drinkware and kitchen utensils
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.teanet = self.add_actor("teanet", "teanet")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        
        # Add distractor objects
        distractor_list = ["calculator", "toycar", "shoe", "dumbbell", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place mug on tray
        success = self.pick_and_place(self.mug, self.tray)
        print("Pick and place mug:", success)
        if not success:
            return self.info
            
        # Place cup_with_handle on tray
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Pick and place cup_with_handle:", success)
        if not success:
            return self.info
            
        # Place teanet on tray
        success = self.pick_and_place(self.teanet, self.tray)
        print("Pick and place teanet:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all required objects are on the tray
        return (
            self.check_on(self.mug, self.tray) and
            self.check_on(self.cup_with_handle, self.tray) and
            self.check_on(self.teanet, self.tray)
        )
