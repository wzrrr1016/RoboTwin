from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 51_hygiene_and_tools_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors
        distractor_list = ['apple', 'chips-tub', 'alarm-clock', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place tissue-box on fluted_block (wrong)
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box on fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Place tissue-box into wooden_box (recovery)
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("Place tissue-box into wooden_box:", success)
        if not success:
            return self.info

        # Step 3: Place shampoo into wooden_box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Place shampoo into wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place screwdriver onto fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver onto fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place knife onto fluted_block
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Place knife onto fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all objects are in their correct containers
        tissue_correct = self.check_on(self.tissue_box, self.wooden_box)
        shampoo_correct = self.check_on(self.shampoo, self.wooden_box)
        screwdriver_correct = self.check_on(self.screwdriver, self.fluted_block)
        knife_correct = self.check_on(self.knife, self.fluted_block)

        return tissue_correct and shampoo_correct and screwdriver_correct and knife_correct
