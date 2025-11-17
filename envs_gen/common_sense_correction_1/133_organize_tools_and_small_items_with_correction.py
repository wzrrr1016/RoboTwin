from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 133_organize_tools_and_small_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.tray = self.add_actor("tray", "tray")

        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.shampoo = self.add_actor("shampoo", "shampoo")

        # Add distractors
        distractor_list = ["apple", "baguette", "book", "shoe", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place hammer in fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Hammer to fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Place small-speaker in tray
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Small-speaker to tray:", success)
        if not success:
            return self.info

        # Step 3: Place shampoo in fluted_block (wrong)
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Shampoo to fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover shampoo to tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Shampoo to tray (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place screwdriver in fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Screwdriver to fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all objects are in the correct containers
        if (
            self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.small_speaker, self.tray) and
            self.check_on(self.shampoo, self.tray)
        ):
            return True
        return False
