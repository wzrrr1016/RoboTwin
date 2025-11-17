from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 217_blocks_and_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add required objects
        self.markpen = self.add_actor("markpen", "markpen")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        
        # Add distractors
        distractor_list = ['calculator', 'pot-with-plant', 'hammer', 'tissue-box', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        # First wrong action: place markpen on tray
        success = self.pick_and_place(self.markpen, self.tray)
        print("Place markpen on tray (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: place markpen on coaster
        success = self.pick_and_place(self.markpen, self.coaster)
        print("Place markpen on coaster (recovery):", success)
        if not success:
            return self.info
            
        # Place blocks on tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Place yellow block:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.green_block, self.tray)
        print("Place green block:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.pink_block, self.tray)
        print("Place pink block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if markpen is on coaster
        if not self.check_on(self.markpen, self.coaster):
            return False
            
        # Check if all blocks are on tray
        if (self.check_on(self.yellow_block, self.tray) and
            self.check_on(self.green_block, self.tray) and
            self.check_on(self.pink_block, self.tray)):
            return True
            
        return False
