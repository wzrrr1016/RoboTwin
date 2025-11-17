from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 363_protect_surface_by_block_grouping_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster as the container
        self.coaster = self.add_actor("coaster", "coaster")
        # Add the solid toy blocks
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.red_block = self.add_actor("red_block", "red_block")
        # Add the metal objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.bell = self.add_actor("bell", "bell")
        # Add distractors
        distractor_list = ["apple", "baguette", "tissue-box", "shoe", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place purple block on coaster
        success = self.pick_and_place(self.purple_block, self.coaster)
        print("Place purple_block:", success)
        if not success:
            return self.info

        # Step 2: Place screwdriver on coaster (wrong action)
        success = self.pick_and_place(self.screwdriver, self.coaster)
        print("Place screwdriver (wrong):", success)
        if not success:
            return self.info

        # Step 3: Move screwdriver from coaster to table (recovery)
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Move screwdriver to table:", success)
        if not success:
            return self.info

        # Step 4: Place red block on coaster
        success = self.pick_and_place(self.red_block, self.coaster)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Step 5: Place bell on table
        success = self.pick_and_place(self.bell, self.table)
        print("Place bell on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if both blocks are on the coaster
        blocks_on_coaster = (
            self.check_on(self.purple_block, self.coaster) and
            self.check_on(self.red_block, self.coaster)
        )
        # Check if metal objects are not on the coaster
        metals_off_coaster = (
            not self.check_on(self.screwdriver, self.coaster) and
            not self.check_on(self.bell, self.coaster)
        )
        return blocks_on_coaster and metals_off_coaster
