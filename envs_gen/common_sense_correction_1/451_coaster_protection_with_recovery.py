from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 451_coaster_protection_with_recovery(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add required objects
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.can = self.add_actor("can", "can")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractor objects
        distractors = ["calculator", "pet-collar", "tissue-box", "shoe", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Place green block on coaster
        success = self.pick_and_place(self.green_block, self.coaster)
        print("Place green_block on coaster:", success)
        if not success:
            return self.info
            
        # Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info
            
        # Incorrectly place dumbbell on coaster (wrong action)
        success = self.pick_and_place(self.dumbbell, self.coaster)
        print("Place dumbbell on coaster (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: Move dumbbell back to table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Move dumbbell to table (recovery):", success)
        if not success:
            return self.info
            
        # Place yellow block on coaster
        success = self.pick_and_place(self.yellow_block, self.coaster)
        print("Place yellow_block on coaster:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if all drink containers and light toys are on the coaster
        # and heavy items are not on the coaster
        if (self.check_on(self.green_block, self.coaster) and
            self.check_on(self.can, self.coaster) and
            self.check_on(self.yellow_block, self.coaster) and
            self.check_on(self.dumbbell, self.table)):
            return True
        return False
