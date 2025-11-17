from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 330_small_toys_vs_disposable_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Create the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Create the toy blocks and tissue-box
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects
        distractors = ["calculator", "olive-oil", "hammer", "pot-with-plant", "shoe"]
        self.add_distractors(distractors)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Initial wrong action: place tissue-box on coaster
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("Wrong placement of tissue-box on coaster:", success)
        if not success:
            return self.info

        # Recovery action: move tissue-box back to table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Recovering tissue-box to table:", success)
        if not success:
            return self.info

        # Place yellow block on coaster
        success = self.pick_and_place(self.yellow_block, self.coaster)
        print("Placing yellow block on coaster:", success)
        if not success:
            return self.info

        # Place blue block on coaster
        success = self.pick_and_place(self.blue_block, self.coaster)
        print("Placing blue block on coaster:", success)
        if not success:
            return self.info

        # Place pink block on coaster
        success = self.pick_and_place(self.pink_block, self.coaster)
        print("Placing pink block on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if all blocks are on the coaster
        blocks_on_coaster = (
            self.check_on(self.yellow_block, self.coaster) and
            self.check_on(self.blue_block, self.coaster) and
            self.check_on(self.pink_block, self.coaster)
        )
        
        # Check if tissue-box is not on the coaster
        tissue_not_on_coaster = not self.check_on(self.tissue_box, self.coaster)
        
        return blocks_on_coaster and tissue_not_on_coaster
