from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 297_hot_drink_and_storage_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add required objects to the environment
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.can = self.add_actor("can", "can")
        self.apple = self.add_actor("apple", "apple")
        
        # Add distractor objects to the environment
        distractor_list = ['calculator', 'screwdriver', 'alarm-clock', 'toycar', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        # First wrong action: place mug into wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Place mug into wooden_box (wrong):", success)
        
        # Recovery action: pick mug from wooden_box and place onto fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Recover mug to fluted_block:", success)
        if not success:
            return self.info

        # Place cup_with_handle (hot-drink vessel) on fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup_with_handle on fluted_block:", success)
        if not success:
            return self.info

        # Place can (sealed metal container) into wooden_box
        success = self.pick_and_place(self.can, self.wooden_box)
        print("Place can into wooden_box:", success)
        if not success:
            return self.info

        # Place apple (perishable food) into wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Place apple into wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.can, self.wooden_box) and
            self.check_on(self.apple, self.wooden_box)
        ):
            return True
        return False
