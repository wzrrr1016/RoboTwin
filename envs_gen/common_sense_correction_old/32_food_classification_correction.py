from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 32_food_classification_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        # Add food items
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.bread = self.add_actor("bread", "bread")
        # Add non-food item (knife) for completeness
        self.knife = self.add_actor("knife", "knife")

    def play_once(self):
        # Pick orange_block from tray and place into fluted_block
        success = self.pick_and_place(self.orange_block, self.fluted_block)
        print("pick place orange_block:", success)
        if not success:
            return self.info

        # Pick bread from table and place into tray
        success = self.pick_and_place(self.bread, self.tray)
        print("pick place bread:", success)
        if not success:
            return self.info

        # Pick hamburg from tray and place into fluted_block
        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("pick place hamburg:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if orange_block is on fluted_block
        if not self.check_on(self.orange_block, self.fluted_block):
            return False
        # Check if hamburg is on fluted_block
        if not self.check_on(self.hamburg, self.fluted_block):
            return False
        # Check if bread is on tray
        if not self.check_on(self.bread, self.tray):
            return False
        return True
