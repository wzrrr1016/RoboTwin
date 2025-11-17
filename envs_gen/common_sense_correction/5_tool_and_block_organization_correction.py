from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 5_tool_and_block_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.bell = self.add_actor("bell", "bell")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'table-tennis', 'jam-jar', 'shoe', 'book']
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Initial wrong placement of blue_block into shoe_box
        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Place blue_block into shoe_box (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: move blue_block to wooden_box
        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("Move blue_block to wooden_box (recovery):", success)
        if not success:
            return self.info
        
        # Place tools into shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Place screwdriver into shoe_box:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.bell, self.shoe_box)
        print("Place bell into shoe_box:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.stapler, self.shoe_box)
        print("Place stapler into shoe_box:", success)
        if not success:
            return self.info
        
        # Place yellow_block into wooden_box
        success = self.pick_and_place(self.yellow_block, self.wooden_box)
        print("Place yellow_block into wooden_box:", success)
        if not success:
            return self.info
        
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all tools are in shoe_box and blocks are in wooden_box
        if (self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.bell, self.shoe_box) and
            self.check_on(self.stapler, self.shoe_box) and
            self.check_on(self.blue_block, self.wooden_box) and
            self.check_on(self.yellow_block, self.wooden_box)):
            return True
        return False
