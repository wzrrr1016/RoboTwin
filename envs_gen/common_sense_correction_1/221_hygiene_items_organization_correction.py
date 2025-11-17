from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 221_hygiene_items_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        # Add the relevant objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.scanner = self.add_actor("scanner", "scanner")
        self.apple = self.add_actor("apple", "apple")
        # Add distractors
        distractor_list = ["hammer", "screwdriver", "toycar", "pot-with-plant", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place tissue-box into fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box:", success)
        if not success:
            return self.info

        # Step 2: Place scanner into fluted_block (wrong action)
        success = self.pick_and_place(self.scanner, self.fluted_block)
        print("Place scanner (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover scanner by placing it on the table
        success = self.pick_and_place(self.scanner, self.table)
        print("Recover scanner:", success)
        if not success:
            return self.info

        # Step 4: Place shampoo into fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Place shampoo:", success)
        if not success:
            return self.info

    def check_success(self):
        if (self.check_on(self.tissue_box, self.fluted_block) and
            self.check_on(self.shampoo, self.fluted_block) and
            self.check_on(self.scanner, self.table)):
            return True
        return False
