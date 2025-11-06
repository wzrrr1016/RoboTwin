from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 43_color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Load objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.bell = self.add_actor("bell", "bell")
        self.mouse = self.add_actor("mouse", "mouse")
        self.toycar = self.add_actor("toycar", "toycar")

    def play_once(self):
        # Pick red_block and place into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("pick place red_block:", success)
        if not success:
            return self.info
        
        # Pick green_block and place into dustbin
        success = self.pick_and_place(self.green_block, self.dustbin)
        print("pick place green_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if red_block is on shoe_box and green_block is on dustbin
        if self.check_on(self.red_block, self.shoe_box) and self.check_on(self.green_block, self.dustbin):
            return True
        return False
