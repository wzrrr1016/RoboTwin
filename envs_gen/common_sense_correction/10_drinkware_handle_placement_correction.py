from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 10_drinkware_handle_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load all required objects and the fluted_block container
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.apple = self.add_actor("apple", "apple")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.microphone = self.add_actor("microphone", "microphone")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

    def play_once(self):
        # Step 1: Pick mug and place into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("pick place mug:", success)
        if not success:
            return self.info

        # Step 2: Pick microphone and place into fluted_block (wrong action)
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("pick place microphone:", success)
        if not success:
            return self.info

        # Step 3: Recovery: Pick microphone from fluted_block and place on table
        if self.check_on(self.microphone, self.fluted_block):
            success = self.pick_and_place(self.microphone, self.table)
            print("pick place microphone on table:", success)
            if not success:
                return self.info

        # Step 4: Pick cup_with_handle and place into fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if both mug and cup_with_handle are on the fluted_block
        if self.check_on(self.mug, self.fluted_block) and self.check_on(self.cup_with_handle, self.fluted_block):
            return True
        return False
