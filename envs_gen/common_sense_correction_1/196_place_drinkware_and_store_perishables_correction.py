from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 196_place_drinkware_and_store_perishables_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")

        # Add distractors
        distractor_list = ["calculator", "screwdriver", "hammer", "toycar", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place mug on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Place mug on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place apple on coaster (wrong action)
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing apple into wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Move apple to wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place bread into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread in wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all conditions are met
        if (
            self.check_on(self.mug, self.coaster) and
            self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.bread, self.wooden_box)
        ):
            return True
        return False
