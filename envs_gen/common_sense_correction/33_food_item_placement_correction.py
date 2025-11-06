from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 33_food_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the wooden_box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Add the objects
        self.bread = self.add_actor("bread", "bread")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.bell = self.add_actor("bell", "bell")

    def play_once(self):
        # Recovery step: pick bell from wooden_box and place on table
        success = self.pick_and_place(self.bell, self.table)
        print("pick place bell (recovery):", success)
        if not success:
            return self.info

        # Correct action: pick bread and place into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("pick place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        return self.check_on(self.bread, self.wooden_box)
