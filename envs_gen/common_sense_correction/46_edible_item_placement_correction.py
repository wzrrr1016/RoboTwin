from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 46_edible_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.tray = self.add_actor("tray", "tray")
        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.knife = self.add_actor("knife", "knife")
        self.toycar = self.add_actor("toycar", "toycar")

    def play_once(self):
        # Attempt to pick up the bread and place it into the tray
        success = self.pick_and_place(self.bread, self.tray)
        print("pick place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the bread is on the tray
        return self.check_on(self.bread, self.tray)
