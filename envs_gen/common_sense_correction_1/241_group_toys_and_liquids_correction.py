from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 241_group_toys_and_liquids_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        
        # Add required objects
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.can = self.add_actor("can", "can")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        
        # Add distractors
        self.add_distractors(["calculator", "hammer", "book", "stapler", "tissue-box"])

    def play_once(self):
        # Initial wrong action: place can on plate
        success = self.pick_and_place(self.can, self.plate)
        print("Pick can and place on plate (wrong):", success)
        if not success:
            return self.info
        
        # Recovery action: move can to tray
        success = self.pick_and_place(self.can, self.tray)
        print("Pick can from plate and place on tray (recovery):", success)
        if not success:
            return self.info
        
        # Place shampoo on tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick shampoo and place on tray:", success)
        if not success:
            return self.info
        
        # Place pot-with-plant on tray
        success = self.pick_and_place(self.pot_with_plant, self.tray)
        print("Pick pot-with-plant and place on tray:", success)
        if not success:
            return self.info
        
        # Place blue block on plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Pick blue_block and place on plate:", success)
        if not success:
            return self.info
        
        # Place orange block on plate
        success = self.pick_and_place(self.orange_block, self.plate)
        print("Pick orange_block and place on plate:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Check if all required objects are in their correct containers
        if (self.check_on(self.blue_block, self.plate) and
            self.check_on(self.orange_block, self.plate) and
            self.check_on(self.can, self.tray) and
            self.check_on(self.shampoo, self.tray) and
            self.check_on(self.pot_with_plant, self.tray)):
            return True
        return False
