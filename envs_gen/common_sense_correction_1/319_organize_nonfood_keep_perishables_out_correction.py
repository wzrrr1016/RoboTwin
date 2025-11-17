from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 319_organize_nonfood_keep_perishables_out_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the simulation environment"""
        # Create the main container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create main objects for the task
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.toycar = self.add_actor("toycar", "toycar")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractor objects to the environment
        distractor_list = ['screwdriver', 'drill', 'calculator', 'alarm-clock', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's actions in the simulation"""
        # Place bottle into fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle:", success)
        if not success:
            return self.info

        # Place tissue-box into fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box:", success)
        if not success:
            return self.info

        # Wrongly place apple into fluted_block (needs recovery)
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Wrongly place apple:", success)
        if not success:
            return self.info

        # Recovery: pick apple from fluted_block and place on table
        success = self.pick_and_place(self.apple, self.table)
        print("Recover apple:", success)
        if not success:
            return self.info

        # Place toycar into fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

        # Place bread on table
        success = self.pick_and_place(self.bread, self.table)
        print("Place bread on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if all non-food items are in the fluted_block
        non_food_in_container = (
            self.check_on(self.tissue_box, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block)
        )
        
        # Check if all perishable foods are NOT in the fluted_block
        food_not_in_container = (
            not self.check_on(self.apple, self.fluted_block) and
            not self.check_on(self.bread, self.fluted_block)
        )
        
        return non_food_in_container and food_not_in_container
