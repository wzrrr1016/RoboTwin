from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 365_drinkware_vs_non_drink_grouping_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create target objects
        self.mug = self.add_actor("mug", "mug")
        self.can = self.add_actor("can", "can")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.green_block = self.add_actor("green_block", "green_block")
        
        # Add distractor objects
        distractor_list = ["calculator", "hammer", "shoe", "book", "microphone"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place drinkware items on tray
        success = self.pick_and_place(self.mug, self.tray)
        print("Pick mug:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.can, self.tray)
        print("Pick can:", success)
        if not success:
            return self.info
            
        # Place non-drink items on fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Pick tissue-box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Pick green_block:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all drinkware items are on tray
        drinkware_on_tray = (
            self.check_on(self.mug, self.tray) and 
            self.check_on(self.can, self.tray)
        )
        
        # Verify non-drink items are on fluted_block
        non_drink_on_fluted = (
            self.check_on(self.tissue_box, self.fluted_block) and 
            self.check_on(self.green_block, self.fluted_block)
        )
        
        return drinkware_on_tray and non_drink_on_fluted
