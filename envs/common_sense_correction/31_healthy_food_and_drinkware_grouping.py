from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_and_drinkware_grouping_31(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.coaster = self.add_actor("coaster", "coaster")
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.bottle = self.add_actor("bottle", "bottle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")

    def play_once(self):
        # Step 1: Place apple into wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Step 2: Place bottle into coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("pick place bottle:", success)
        if not success:
            return self.info

        # Step 3: Place french_fries into wooden_box (wrong, then move to coaster)
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("pick place french_fries into wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Move french_fries from wooden_box to coaster
        success = self.pick_and_place(self.french_fries, self.coaster)
        print("pick place french_fries into coaster:", success)
        if not success:
            return self.info

        # Step 5: Place cup_with_handle into coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info

        # Step 6: Place mug into coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("pick place mug:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if apple is in wooden_box
        if not self.check_on(self.apple, self.wooden_box):
            return False
        # Check if bottle is in coaster
        if not self.check_on(self.bottle, self.coaster):
            return False
        # Check if french_fries is in coaster
        if not self.check_on(self.french_fries, self.coaster):
            return False
        # Check if cup_with_handle is in coaster
        if not self.check_on(self.cup_with_handle, self.coaster):
            return False
        # Check if mug is in coaster
        if not self.check_on(self.mug, self.coaster):
            return False
        return True
