from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 24_food_and_hazard_placement_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create required objects
        self.knife = self.add_actor("knife", "knife")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.bottle = self.add_actor("bottle", "bottle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractors
        distractor_list = ['toycar', 'pot-with-plant', 'book', 'shoe', 'red_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place food and drinkware on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french_fries on tray:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.bottle, self.tray)
        print("Place bottle on tray:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Place cup_with_handle on tray:", success)
        if not success:
            return self.info
            
        # Place sharp/electronic items in fluted_block
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Place small-speaker in fluted_block:", success)
        if not success:
            return self.info
            
        # Wrong placement of knife (on tray)
        success = self.pick_and_place(self.knife, self.tray)
        print("Place knife on tray (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: move knife to correct container
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Move knife to fluted_block:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all objects are in correct containers
        if (self.check_on(self.french_fries, self.tray) and
            self.check_on(self.bottle, self.tray) and
            self.check_on(self.cup_with_handle, self.tray) and
            self.check_on(self.small_speaker, self.fluted_block) and
            self.check_on(self.knife, self.fluted_block)):
            return True
        return False
