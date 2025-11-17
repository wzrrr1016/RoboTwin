from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 460_place_edible_items_with_one_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bottle = self.add_actor("bottle", "bottle")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add distractors
        distractor_list = ['hammer', 'shoe', 'book', 'toycar', 'microphone']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick apple and place into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick apple:", success)
        if not success:
            return self.info

        # Step 2: Pick bottle and place into fluted_block (wrong)
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Pick bottle (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing bottle on table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle:", success)
        if not success:
            return self.info

        # Step 4: Pick french_fries and place into fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Pick french fries:", success)
        if not success:
            return self.info

        # Step 5: Pick blue_block and place on table
        success = self.pick_and_place(self.blue_block, self.table)
        print("Pick blue block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if edible items (apple and french_fries) are in the fluted_block
        apple_on = self.check_on(self.apple, self.fluted_block)
        fries_on = self.check_on(self.french_fries, self.fluted_block)
        
        # Ensure non-edible items (bottle and blue_block) are not in the fluted_block
        bottle_not_on = not self.check_on(self.bottle, self.fluted_block)
        blue_not_on = not self.check_on(self.blue_block, self.fluted_block)
        
        return apple_on and fries_on and bottle_not_on and blue_not_on
