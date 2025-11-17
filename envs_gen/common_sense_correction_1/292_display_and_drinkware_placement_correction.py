from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 292_display_and_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.tray = self.add_actor("tray", "tray")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Create relevant objects
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.markpen = self.add_actor("markpen", "markpen")
        self.cup = self.add_actor("cup", "cup")
        
        # Add distractors
        distractor_list = ["shoe", "dumbbell", "toycar", "hammer", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place pot-with-plant on tray
        success = self.pick_and_place(self.pot_with_plant, self.tray)
        print("Place pot-with-plant on tray:", success)
        if not success:
            return self.info
        
        # Place small-speaker on tray
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Place small-speaker on tray:", success)
        if not success:
            return self.info
        
        # Wrongly place cup on tray (needs recovery)
        success = self.pick_and_place(self.cup, self.tray)
        print("Wrongly place cup on tray:", success)
        if not success:
            return self.info
        
        # Recovery: move cup to coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Move cup to coaster:", success)
        if not success:
            return self.info
        
        # Place markpen on tray
        success = self.pick_and_place(self.markpen, self.tray)
        print("Place markpen on tray:", success)
        if not success:
            return self.info
        
        return self.info  # Return info on successful completion

    def check_success(self):
        # Verify all required objects are in the correct containers
        if (self.check_on(self.pot_with_plant, self.tray) and
            self.check_on(self.small_speaker, self.tray) and
            self.check_on(self.markpen, self.tray) and
            self.check_on(self.cup, self.coaster)):
            return True
        return False
