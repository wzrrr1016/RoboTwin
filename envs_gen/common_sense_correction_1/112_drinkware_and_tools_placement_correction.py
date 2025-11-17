from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 112_drinkware_and_tools_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.cup = self.add_actor("cup", "cup")
        self.teanet = self.add_actor("teanet", "teanet")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'toycar', 'book', 'pot-with-plant']
        self.add_distractors(distractor_list)

    def play_once(self):
        # First wrong action: place cup on fluted_block
        success = self.pick_and_place(self.cup, self.fluted_block)
        print("Pick cup and place on fluted_block (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: pick cup from fluted_block and place on tray
        success = self.pick_and_place(self.cup, self.tray)
        print("Pick cup and place on tray (recovery):", success)
        if not success:
            return self.info
        
        # Place bread on tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread and place on tray:", success)
        if not success:
            return self.info
        
        # Place teanet on tray
        success = self.pick_and_place(self.teanet, self.tray)
        print("Pick teanet and place on tray:", success)
        if not success:
            return self.info
        
        # Place screwdriver on fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Pick screwdriver and place on fluted_block:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Check if all eating/drinking items are on tray and screwdriver on fluted_block
        if (
            self.check_on(self.bread, self.tray) and
            self.check_on(self.cup, self.tray) and
            self.check_on(self.teanet, self.tray) and
            self.check_on(self.screwdriver, self.fluted_block)
        ):
            return True
        return False
