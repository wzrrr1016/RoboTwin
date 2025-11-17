from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 94_hot_drinkware_and_perishables_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.apple = self.add_actor("apple", "apple")

        # Add distractors
        distractor_list = ["calculator", "toycar", "shoe", "book", "hammer"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: apple to fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick apple and place on fluted_block (wrong):", success)
        if not success:
            return self.info

        # Recovery: apple to wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Pick apple from fluted_block and place into wooden_box (recovery):", success)
        if not success:
            return self.info

        # Correct placements
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Pick cup_with_handle and place on fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Pick mug and place on fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_without_handle, self.wooden_box)
        print("Pick cup_without_handle and place into wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        if (
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.cup_without_handle, self.wooden_box) and
            self.check_on(self.apple, self.wooden_box)
        ):
            return True
        return False
