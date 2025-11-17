from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 130_store_toys_and_blocks_correction(Imagine_Task):
    def load_actors(self):
        # Add container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add required objects
        self.apple = self.add_actor("apple", "apple")
        self.toycar = self.add_actor("toycar", "toycar")
        self.green_block = self.add_actor("green_block", "green_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'tissue-box', 'small-speaker', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Pick and place toycar
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Pick toycar:", success)
        if not success:
            return self.info
            
        # Pick and place green block
        success = self.pick_and_place(self.green_block, self.shoe_box)
        print("Pick green_block:", success)
        if not success:
            return self.info
            
        # Pick and place purple block
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("Pick purple_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all required objects are in the shoe_box
        if (self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.green_block, self.shoe_box) and
            self.check_on(self.purple_block, self.shoe_box)):
            return True
        return False
