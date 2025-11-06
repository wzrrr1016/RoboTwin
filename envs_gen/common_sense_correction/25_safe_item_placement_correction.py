from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 25_safe_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the shoe_box as a container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        # Add the non-dangerous items
        self.toycar = self.add_actor("toycar", "toycar")
        self.scanner = self.add_actor("scanner", "scanner")
        self.fork = self.add_actor("fork", "fork")
        self.apple = self.add_actor("apple", "apple")
        # Add the dangerous item
        self.knife = self.add_actor("knife", "knife")

    def play_once(self):
        # Check if the knife is already in the shoe_box (wrong action)
        if self.check_on(self.knife, self.shoe_box):
            # Pick the knife and place it on the table (recovery)
            success = self.pick_and_place(self.knife, self.table)
            print("pick place knife:", success)
            if not success:
                return self.info

        # Now place the fork into the shoe_box (correct action)
        success = self.pick_and_place(self.fork, self.shoe_box)
        print("pick place fork:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the fork is in the shoe_box and the knife is not
        if self.check_on(self.fork, self.shoe_box) and not self.check_on(self.knife, self.shoe_box):
            return True
        return False
