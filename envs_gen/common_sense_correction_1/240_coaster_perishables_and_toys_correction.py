from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 240_coaster_perishables_and_toys_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add perishable food objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        
        # Add small toy blocks
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractor objects
        distractor_list = ["calculator", "screwdriver", "pot-with-plant", "alarm-clock", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's actions in sequence"""
        # Place apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster:", success)
        if not success:
            return self.info

        # Place blue_block on coaster (wrong action)
        success = self.pick_and_place(self.blue_block, self.coaster)
        print("Place blue_block on coaster (wrong):", success)
        if not success:
            return self.info

        # Recover blue_block to table
        success = self.pick_and_place(self.blue_block, self.table)
        print("Recover blue_block to table:", success)
        if not success:
            return self.info

        # Place bread on coaster
        success = self.pick_and_place(self.bread, self.coaster)
        print("Place bread on coaster:", success)
        if not success:
            return self.info

        # Place yellow_block on table
        success = self.pick_and_place(self.yellow_block, self.table)
        print("Place yellow_block on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if perishable foods are on the coaster
        apple_on_coaster = self.check_on(self.apple, self.coaster)
        bread_on_coaster = self.check_on(self.bread, self.coaster)
        
        # Check if blocks are not on the coaster
        blue_off_coaster = not self.check_on(self.blue_block, self.coaster)
        yellow_off_coaster = not self.check_on(self.yellow_block, self.coaster)
        
        # Return True only if all conditions are met
        return all([
            apple_on_coaster,
            bread_on_coaster,
            blue_off_coaster,
            yellow_off_coaster
        ])
