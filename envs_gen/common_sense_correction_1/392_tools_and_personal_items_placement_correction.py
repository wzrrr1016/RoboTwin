from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 392_tools_and_personal_items_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.hammer = self.add_actor("hammer", "hammer")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.markpen = self.add_actor("markpen", "markpen")

        # Add distractors
        distractor_list = ["toycar", "pot-with-plant", "alarm-clock", "dumbbell", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrong placement of markpen into wooden_box
        success = self.pick_and_place(self.markpen, self.wooden_box)
        print("Pick markpen and place into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - move markpen to fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Pick markpen from wooden_box and place onto fluted_block (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place screwdriver into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Pick screwdriver and place into wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place shampoo onto fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Pick shampoo and place onto fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place hammer into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Pick hammer and place into wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required objects are in their correct containers
        if (
            self.check_on(self.screwdriver, self.wooden_box) and
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.shampoo, self.fluted_block) and
            self.check_on(self.markpen, self.fluted_block)
        ):
            return True
        return False
