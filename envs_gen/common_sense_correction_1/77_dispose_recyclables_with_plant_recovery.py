from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 77_dispose_recyclables_with_plant_recovery(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add main objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bottle = self.add_actor("bottle", "bottle")
        self.stapler = self.add_actor("stapler", "stapler")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        
        # Add distractors
        distractor_list = ['baguette', 'apple', 'french_fries', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions"""
        # Correct action: Tissue box to dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Tissue-box to dustbin:", success)
        if not success:
            return self.info

        # Wrong action: Pot with plant to dustbin
        success = self.pick_and_place(self.pot_with_plant, self.dustbin)
        print("Pot-with-plant to dustbin (wrong):", success)
        if not success:
            return self.info

        # Recovery action: Pot with plant to table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Pot-with-plant to table (recovery):", success)
        if not success:
            return self.info

        # Correct action: Bottle to dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Bottle to dustbin:", success)
        if not success:
            return self.info

        # Correct action: Stapler to table
        success = self.pick_and_place(self.stapler, self.table)
        print("Stapler to table:", success)
        if not success:
            return self.info

        # Correct action: Yellow block to table
        success = self.pick_and_place(self.yellow_block, self.table)
        print("Yellow_block to table:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        return (
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.pot_with_plant, self.table) and
            self.check_on(self.stapler, self.table) and
            self.check_on(self.yellow_block, self.table)
        )
