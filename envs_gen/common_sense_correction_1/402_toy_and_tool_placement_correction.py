from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 402_toy_and_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        
        # Add objects
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractors
        distractor_list = ["book", "shoe", "pot-with-plant", "alarm-clock", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place blue_block on plate (correct)
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Place blue_block on plate:", success)
        if not success:
            return self.info
            
        # Step 2: Place hammer on plate (wrong action)
        success = self.pick_and_place(self.hammer, self.plate)
        print("Place hammer on plate (wrong):", success)
        if not success:
            return self.info
            
        # Step 3: Recover by placing hammer on tray
        success = self.pick_and_place(self.hammer, self.tray)
        print("Place hammer on tray (recovery):", success)
        if not success:
            return self.info
            
        # Step 4: Place yellow_block on plate (correct)
        success = self.pick_and_place(self.yellow_block, self.plate)
        print("Place yellow_block on plate:", success)
        if not success:
            return self.info
            
        # Step 5: Place screwdriver on tray (correct)
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Place screwdriver on tray:", success)
        if not success:
            return self.info
            
        # Step 6: Place purple_block on plate (correct)
        success = self.pick_and_place(self.purple_block, self.plate)
        print("Place purple_block on plate:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Check all lightweight toys (blocks) are on the plate
        blocks_on_plate = (
            self.check_on(self.blue_block, self.plate) and
            self.check_on(self.yellow_block, self.plate) and
            self.check_on(self.purple_block, self.plate)
        )
        
        # Check all heavy tools are on the tray
        tools_on_tray = (
            self.check_on(self.hammer, self.tray) and
            self.check_on(self.screwdriver, self.tray)
        )
        
        return blocks_on_plate and tools_on_tray
