from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 4_shoe_and_shampoo_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Load objects
        self.shoe = self.add_actor("shoe", "shoe")
        self.shampoo = self.add_actor("shampoo", "shampoo")

    def play_once(self):
        # Step 1: Pick shoe and place into shoe_box
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Pick and place shoe:", success)
        if not success:
            return self.info

        # Step 2: Pick shampoo and place into dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Pick and place shampoo:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if shoe is on shoe_box and shampoo is on dustbin
        if self.check_on(self.shoe, self.shoe_box) and self.check_on(self.shampoo, self.dustbin):
            return True
        return False
