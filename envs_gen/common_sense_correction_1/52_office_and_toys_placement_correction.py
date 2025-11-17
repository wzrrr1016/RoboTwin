from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 52_office_and_toys_placement_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create target objects
        self.mouse = self.add_actor("mouse", "mouse")
        self.scanner = self.add_actor("scanner", "scanner")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.teanet = self.add_actor("teanet", "teanet")
        
        # Add distractors
        distractor_list = ["dumbbell", "shoe", "book", "pot-with-plant", "hammer"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place compact electronic office devices in wooden_box
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Place mouse in wooden_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("Place scanner in wooden_box:", success)
        if not success:
            return self.info
            
        # Wrong placement of purple_block (will be corrected)
        success = self.pick_and_place(self.purple_block, self.wooden_box)
        print("Wrong placement of purple_block:", success)
        if not success:
            return self.info
            
        # Recovery - move purple_block to correct container
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Recover purple_block to fluted_block:", success)
        if not success:
            return self.info
            
        # Place remaining objects in fluted_block
        success = self.pick_and_place(self.pink_block, self.fluted_block)
        print("Place pink_block in fluted_block:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.teanet, self.fluted_block)
        print("Place teanet in fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        return (
            self.check_on(self.mouse, self.wooden_box) and
            self.check_on(self.scanner, self.wooden_box) and
            self.check_on(self.purple_block, self.fluted_block) and
            self.check_on(self.pink_block, self.fluted_block) and
            self.check_on(self.teanet, self.fluted_block)
        )
