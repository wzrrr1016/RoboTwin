from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 477_food_and_drinkware_tray_placement_correction(Imagine_Task):
    def load_actors(self):
        self.tray = self.add_actor("tray", "tray")
        self.bread = self.add_actor("bread", "bread")
        self.mug = self.add_actor("mug", "mug")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        distractor_list = ["calculator", "screwdriver", "shoe", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mug, self.tray)
        print("Pick mug:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.orange_block, self.tray)
        print("Pick orange_block (wrong):", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.orange_block, self.table)
        print("Recover orange_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        if (self.check_on(self.bread, self.tray) and 
            self.check_on(self.mug, self.tray) and 
            not self.check_on(self.orange_block, self.tray)):
            return True
        return False
