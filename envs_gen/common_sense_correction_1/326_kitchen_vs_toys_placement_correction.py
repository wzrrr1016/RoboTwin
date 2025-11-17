from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 326_kitchen_vs_toys_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        
        # Add required objects
        self.teanet = self.add_actor("teanet", "teanet")
        self.can = self.add_actor("can", "can")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.green_block = self.add_actor("green_block", "green_block")
        
        # Add distractors
        distractor_list = ["screwdriver", "hammer", "shoe", "dumbbell", "calculator"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place teanet on plate (small kitchen drink-related item)
        success = self.pick_and_place(self.teanet, self.plate)
        print("Pick teanet to plate:", success)
        if not success:
            return self.info
            
        # Wrong placement of can (should be on plate)
        success = self.pick_and_place(self.can, self.tray)
        print("Pick can to tray (wrong):", success)
        if not success:
            return self.info
            
        # Recovery - place can on correct container
        success = self.pick_and_place(self.can, self.plate)
        print("Recover can to plate:", success)
        if not success:
            return self.info
            
        # Place toys/decorative items on tray
        success = self.pick_and_place(self.sand_clock, self.tray)
        print("Pick sand-clock to tray:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.pink_block, self.tray)
        print("Pick pink_block to tray:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.green_block, self.tray)
        print("Pick green_block to tray:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        return (
            self.check_on(self.teanet, self.plate) and
            self.check_on(self.can, self.plate) and
            self.check_on(self.sand_clock, self.tray) and
            self.check_on(self.pink_block, self.tray) and
            self.check_on(self.green_block, self.tray)
        )
