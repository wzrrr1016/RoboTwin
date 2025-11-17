from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 40_tool_and_electronics_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.hammer = self.add_actor("hammer", "hammer")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add distractors
        distractor_list = ["chips-tub", "apple", "book", "shoe", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place small-speaker on fluted_block
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Place small-speaker:", success)
        if not success:
            return self.info

        # Step 2: Place screwdriver in wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        # Step 3: Place shampoo in wooden_box (wrong placement)
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Place shampoo (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover shampoo to fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Recover shampoo:", success)
        if not success:
            return self.info

        # Step 5: Place hammer in wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Place hammer:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all objects are in their correct locations
        if (self.check_on(self.screwdriver, self.wooden_box) and
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.small_speaker, self.fluted_block) and
            self.check_on(self.shampoo, self.fluted_block)):
            return True
        return False
