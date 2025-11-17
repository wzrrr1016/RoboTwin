from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 425_handheld_electronics_and_tools_placement_correction(Imagine_Task):
    def load_actors(self):
        # Create the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Create the main objects
        self.apple = self.add_actor("apple", "apple")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.mouse = self.add_actor("mouse", "mouse")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractor objects to the environment
        distractors = ["pot-with-plant", "book", "shoe", "tissue-box", "red_block"]
        self.add_distractors(distractors)

    def play_once(self):
        # First wrong action: try to place apple on tray (should fail)
        success = self.pick_and_place(self.apple, self.tray)
        print("Pick apple into tray (wrong):", success)
        
        # If the wrong action failed, perform recovery by placing apple on table
        if not success:
            success = self.pick_and_place(self.apple, self.table)
            print("Recovery: apple to table:", success)
            if not success:
                return self.info
        
        # Place mouse on tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("Pick mouse into tray:", success)
        if not success:
            return self.info
        
        # Place small speaker on tray
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Pick small-speaker into tray:", success)
        if not success:
            return self.info
        
        # Place screwdriver on tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Pick screwdriver into tray:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Check that apple is NOT on the tray (perishable food)
        apple_on_tray = self.check_on(self.apple, self.tray)
        
        # Check that tools and electronics are on the tray
        screwdriver_on_tray = self.check_on(self.screwdriver, self.tray)
        mouse_on_tray = self.check_on(self.mouse, self.tray)
        speaker_on_tray = self.check_on(self.small_speaker, self.tray)
        
        # Return True only if all conditions are met
        return not apple_on_tray and screwdriver_on_tray and mouse_on_tray and speaker_on_tray
