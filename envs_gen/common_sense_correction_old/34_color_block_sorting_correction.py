from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 34_color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load objects
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.apple = self.add_actor("apple", "apple")
        self.mug = self.add_actor("mug", "mug")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.drill = self.add_actor("drill", "drill")

    def play_once(self):
        # Step 1: Pick blue_block and place into wooden_box (incorrect per task, but per action list)
        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Step 2: Pick apple and place into shoe_box (incorrect per task, but per action list)
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Step 3: Pick apple from shoe_box and place into wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("pick place apple again:", success)
        if not success:
            return self.info

        # Step 4: Pick mug and place into shoe_box
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("pick place mug:", success)
        if not success:
            return self.info

        # Step 5: Pick french_fries and place into wooden_box
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("pick place french_fries:", success)
        if not success:
            return self.info

        # Step 6: Pick cup_without_handle and place into shoe_box
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("pick place cup_without_handle:", success)
        if not success:
            return self.info

        # Step 7: Pick drill and place into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("pick place drill:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if blue_block is in shoe_box (correct per task)
        if not self.check_on(self.blue_block, self.shoe_box):
            return False

        # Check if apple is in wooden_box (correct per task)
        if not self.check_on(self.apple, self.wooden_box):
            return False

        # Check if mug is in shoe_box (correct per task)
        if not self.check_on(self.mug, self.shoe_box):
            return False

        # Check if french_fries is in wooden_box (correct per task)
        if not self.check_on(self.french_fries, self.wooden_box):
            return False

        # Check if cup_without_handle is in shoe_box (correct per task)
        if not self.check_on(self.cup_without_handle, self.shoe_box):
            return False

        # Check if drill is in wooden_box (correct per task)
        if not self.check_on(self.drill, self.wooden_box):
            return False

        return True
