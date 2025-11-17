from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 346_organize_eatables_and_keep_sharp_separate_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        # Add the objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.knife = self.add_actor("knife", "knife")
        # Add distractors
        distractor_list = ["calculator", "pet-collar", "toycar", "alarm-clock", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place apple into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info

        # Step 2: Place knife into fluted_block (wrong action)
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Place knife (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recovery - place knife on table
        success = self.pick_and_place(self.knife, self.table)
        print("Recover knife:", success)
        if not success:
            return self.info

        # Step 4: Place french fries into fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french fries:", success)
        if not success:
            return self.info

        # Step 5: Place cup_without_handle into fluted_block
        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("Place cup:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check all required objects are on the fluted_block and knife is not
        apple_on = self.check_on(self.apple, self.fluted_block)
        fries_on = self.check_on(self.french_fries, self.fluted_block)
        cup_on = self.check_on(self.cup_without_handle, self.fluted_block)
        knife_not_on = not self.check_on(self.knife, self.fluted_block)
        return apple_on and fries_on and cup_on and knife_not_on
