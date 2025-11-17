from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 15_block_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add required objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.apple = self.add_actor("apple", "apple")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractors
        distractor_list = ["calculator", "pet-collar", "sand-clock", "toycar", "pot-with-plant", "hammer"]
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Place blocks into wooden_box
        success = self.pick_and_place(self.red_block, self.wooden_box)
        print("Place red_block:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("Place blue_block:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.green_block, self.wooden_box)
        print("Place green_block:", success)
        if not success:
            return self.info
            
        # Wrong placement of apple (part of task sequence)
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Place apple (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: place apple on table
        success = self.pick_and_place(self.apple, self.table)
        print("Place apple on table:", success)
        if not success:
            return self.info
            
        # Place tissue-box on table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Place tissue-box on table:", success)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all blocks in wooden_box and other items on table
        if (self.check_on(self.red_block, self.wooden_box) and
            self.check_on(self.blue_block, self.wooden_box) and
            self.check_on(self.green_block, self.wooden_box) and
            self.check_on(self.apple, self.table) and
            self.check_on(self.tissue_box, self.table)):
            return True
        return False
