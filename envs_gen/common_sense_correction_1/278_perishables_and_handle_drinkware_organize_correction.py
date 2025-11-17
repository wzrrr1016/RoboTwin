from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 278_perishables_and_handle_drinkware_organize_correction(Imagine_Task):
    def load_actors(self):
        # Add the organizer surface
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        # Add required objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "shoe", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrong action - place cup into fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Wrong placement of cup_with_handle:", success)
        if not success:
            return self.info

        # Step 2: Recovery action - place cup on fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Recovery placement of cup_with_handle:", success)
        if not success:
            return self.info

        # Step 3: Place apple on fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info

        # Step 4: Place bread on fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required objects are on the fluted_block
        return (
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block)
        )
