from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 22_non_food_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add all required actors
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.scanner = self.add_actor("scanner", "scanner")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.bread = self.add_actor("bread", "bread")
        self.orange_block = self.add_actor("orange_block", "orange_block")

    def play_once(self):
        # Step 1: Place scanner into wooden_box
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("pick place scanner:", success)
        if not success:
            return self.info

        # Step 2: Place shampoo into wooden_box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("pick place shampoo:", success)
        if not success:
            return self.info

        # Step 3: Place bread into wooden_box (wrong)
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("pick place bread:", success)
        if not success:
            return self.info

        # Step 4: Recover bread from wooden_box and place on table
        success = self.pick_and_place(self.bread, self.table)
        print("recover bread:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if non-food items (scanner, shampoo, orange_block) are in wooden_box
        if (self.check_on(self.scanner, self.wooden_box) and
            self.check_on(self.shampoo, self.wooden_box) and
            self.check_on(self.orange_block, self.wooden_box)):
            # Check if bread is not in wooden_box
            if not self.check_on(self.bread, self.wooden_box):
                return True
        return False
