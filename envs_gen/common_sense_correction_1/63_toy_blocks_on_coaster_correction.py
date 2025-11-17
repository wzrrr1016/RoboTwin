from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 63_toy_blocks_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the coaster, toy blocks, perishable foods, and distractors.
        """
        # Create the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Create toy blocks (small, lightweight objects)
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Create perishable food items
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects to the environment
        distractor_list = ["dumbbell", "shoe", "pot-with-plant", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Place all toy blocks on the coaster
        2. Check and recover any perishable foods mistakenly placed on the coaster
        """
        # Place each toy block on the coaster
        success = self.pick_and_place(self.blue_block, self.coaster)
        print("Place blue block:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.purple_block, self.coaster)
        print("Place purple block:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.yellow_block, self.coaster)
        print("Place yellow block:", success)
        if not success:
            return self.info

        # Recovery actions for perishable foods
        if self.check_on(self.apple, self.coaster):
            success = self.pick_and_place(self.apple, self.table)
            print("Recover apple:", success)
            if not success:
                return self.info

        if self.check_on(self.bread, self.coaster):
            success = self.pick_and_place(self.bread, self.table)
            print("Recover bread:", success)
            if not success:
                return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - All toy blocks are on the coaster
        - No perishable foods are on the coaster
        """
        # Check if all blocks are on the coaster
        blocks_on_coaster = (
            self.check_on(self.blue_block, self.coaster) and
            self.check_on(self.purple_block, self.coaster) and
            self.check_on(self.yellow_block, self.coaster)
        )
        
        # Check if perishable foods are not on the coaster
        perishables_off_coaster = (
            not self.check_on(self.apple, self.coaster) and
            not self.check_on(self.bread, self.coaster)
        )
        
        return blocks_on_coaster and perishables_off_coaster
