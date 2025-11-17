from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 66_organize_perishables_and_small_solids_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors and distractors in the environment"""
        # Add containers to the environment
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add task-specific objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.bottle = self.add_actor("bottle", "bottle")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add distractor objects
        distractor_list = ["calculator", "book", "shoe", "alarm-clock", "microphone"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's sorting actions in sequence"""
        # Initial incorrect placement (to be recovered)
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Initial apple placement (wrong):", success)
        if not success:
            return self.info

        # Recovery action - move apple to correct container
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Apple recovery to fluted_block:", success)
        if not success:
            return self.info

        # Place perishable bread in fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Bread placement:", success)
        if not success:
            return self.info

        # Place small hard purple_block in dustbin
        success = self.pick_and_place(self.purple_block, self.dustbin)
        print("Purple block placement:", success)
        if not success:
            return self.info

        # Place bottle (small hard object) in dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Bottle placement:", success)
        if not success:
            return self.info

        return self.info  # Return final status if all steps succeeded

    def check_success(self):
        """Verify if all objects are in their correct final positions"""
        return (
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.purple_block, self.dustbin) and
            self.check_on(self.bottle, self.dustbin)
        )
