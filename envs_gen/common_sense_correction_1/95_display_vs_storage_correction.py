from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 95_display_vs_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add target objects
        self.book = self.add_actor("book", "book")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors
        distractors = ["dumbbell", "shoe", "stapler", "microphone", "scanner"]
        self.add_distractors(distractors)

    def play_once(self):
        # Step 1: Place pot-with-plant into wooden_box (wrong)
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Place pot-with-plant into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recover by placing pot-with-plant onto fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Recover pot-with-plant to fluted_block:", success)
        if not success:
            return self.info

        # Step 3: Place book onto fluted_block
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Place book onto fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Place shampoo into wooden_box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Place shampoo into wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place toycar into wooden_box
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("Place toycar into wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all objects are in the correct containers
        if (
            self.check_on(self.pot_with_plant, self.fluted_block) and
            self.check_on(self.book, self.fluted_block) and
            self.check_on(self.shampoo, self.wooden_box) and
            self.check_on(self.toycar, self.wooden_box)
        ):
            return True
        return False
