from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 498_serve_edible_on_tray_with_one_correction(Imagine_Task):
    def load_actors(self):
        # Create required containers and objects
        self.tray = self.add_actor("tray", "tray")
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.knife = self.add_actor("knife", "knife")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "pet-collar", "roll-paper", "alarm-clock", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place bread on tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Place bread on tray:", success)
        if not success:
            return self.info
            
        # Wrongly place orange_block on tray then recover
        success = self.pick_and_place(self.orange_block, self.tray)
        print("Wrongly place orange_block on tray:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.orange_block, self.table)
        print("Recover orange_block to table:", success)
        if not success:
            return self.info
            
        # Place french_fries on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french_fries on tray:", success)
        if not success:
            return self.info
            
        # Place knife on table
        success = self.pick_and_place(self.knife, self.table)
        print("Place knife on table:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if edible items are on tray
        bread_on_tray = self.check_on(self.bread, self.tray)
        fries_on_tray = self.check_on(self.french_fries, self.tray)
        
        # Check if non-edible items are not on tray
        knife_not_on_tray = not self.check_on(self.knife, self.tray)
        orange_not_on_tray = not self.check_on(self.orange_block, self.tray)
        
        return bread_on_tray and fries_on_tray and knife_not_on_tray and orange_not_on_tray
