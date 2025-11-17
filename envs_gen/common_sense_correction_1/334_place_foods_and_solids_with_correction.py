from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 334_place_foods_and_solids_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.red_block = self.add_actor("red_block", "red_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractors
        distractor_list = ["calculator", "shoe", "book", "alarm-clock", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place apple on tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Place apple:", success)
        if not success:
            return self.info

        # Step 2: Place red_block on fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Step 3: Place hammer on tray (wrong action)
        success = self.pick_and_place(self.hammer, self.tray)
        print("Place hammer (wrong):", success)
        if not success:
            return self.info

        # Step 4: Move hammer from tray to fluted_block (recovery)
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Recover hammer:", success)
        if not success:
            return self.info

        # Step 5: Place pink_block on fluted_block
        success = self.pick_and_place(self.pink_block, self.fluted_block)
        print("Place pink_block:", success)
        if not success:
            return self.info

        # Step 6: Place hamburg on tray
        success = self.pick_and_place(self.hamburg, self.tray)
        print("Place hamburg:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        # Check if edible foods are on the tray
        edible_on_tray = self.check_on(self.apple, self.tray) and self.check_on(self.hamburg, self.tray)
        
        # Check if solid toys and hand tools are on fluted_block
        tools_on_fluted = (
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.pink_block, self.fluted_block) and
            self.check_on(self.hammer, self.fluted_block)
        )
        
        return edible_on_tray and tools_on_fluted
