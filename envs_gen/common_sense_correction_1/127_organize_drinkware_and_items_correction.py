from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 127_organize_drinkware_and_items_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Create required objects
        self.can = self.add_actor("can", "can")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.bread = self.add_actor("bread", "bread")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors
        distractor_list = ['calculator', 'toycar', 'shoe', 'book', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place screwdriver on coaster (wrong)
        success = self.pick_and_place(self.screwdriver, self.coaster)
        print("Pick screwdriver and place on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - place screwdriver on fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Pick screwdriver from coaster and place on fluted_block (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Pick can and place on coaster:", success)
        if not success:
            return self.info

        # Step 4: Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Pick cup_with_handle and place on coaster:", success)
        if not success:
            return self.info

        # Step 5: Place bread on fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Pick bread and place on fluted_block:", success)
        if not success:
            return self.info

        # Step 6: Place cup_without_handle on coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Pick cup_without_handle and place on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required objects are in the correct containers
        if (
            self.check_on(self.can, self.coaster) and
            self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.cup_without_handle, self.coaster) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block)
        ):
            return True
        return False
