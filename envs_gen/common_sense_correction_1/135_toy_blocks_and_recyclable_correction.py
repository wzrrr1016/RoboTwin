from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 135_toy_blocks_and_recyclable_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add solid colorful toy blocks
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add recyclable metal container
        self.can = self.add_actor("can", "can")

        # Add distractors
        distractor_list = ["calculator", "pot-with-plant", "book", "shoe", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        This includes a wrong action followed by a recovery, and placing blocks on the plate.
        """
        # Wrong action: place can on plate
        success = self.pick_and_place(self.can, self.plate)
        print("Pick can and place into plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: pick can from plate and place into dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Pick can from plate and place into dustbin (recovery):", success)
        if not success:
            return self.info

        # Place blocks on the plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Pick blue_block and place into plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.plate)
        print("Pick green_block and place into plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.yellow_block, self.plate)
        print("Pick yellow_block and place into plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed.
        All blocks must be on the plate and the can must be in the dustbin.
        """
        # Check if all blocks are on the plate
        blocks_on_plate = (
            self.check_on(self.blue_block, self.plate) and
            self.check_on(self.green_block, self.plate) and
            self.check_on(self.yellow_block, self.plate)
        )

        # Check if the can is in the dustbin
        can_in_dustbin = self.check_on(self.can, self.dustbin)

        # Return True only if all conditions are met
        return blocks_on_plate and can_in_dustbin
