from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 406_perishable_vs_solid_disposal_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment."""
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.knife = self.add_actor("knife", "knife")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "pet-collar", "shampoo", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Define the sequence of robot actions to complete the task."""
        # 1. Wrong action: Place bread into dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Pick bread to dustbin (wrong):", success)
        if not success:
            return self.info

        # 2. Recovery: Move bread from dustbin to coaster
        success = self.pick_and_place(self.bread, self.coaster)
        print("Recover bread to coaster:", success)
        if not success:
            return self.info

        # 3. Place knife into dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Pick knife to dustbin:", success)
        if not success:
            return self.info

        # 4. Place blue_block into dustbin
        success = self.pick_and_place(self.blue_block, self.dustbin)
        print("Pick blue_block to dustbin:", success)
        if not success:
            return self.info

        # 5. Place yellow_block into dustbin
        success = self.pick_and_place(self.yellow_block, self.dustbin)
        print("Pick yellow_block to dustbin:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        return (
            self.check_on(self.bread, self.coaster) and
            self.check_on(self.knife, self.dustbin) and
            self.check_on(self.blue_block, self.dustbin) and
            self.check_on(self.yellow_block, self.dustbin)
        )
