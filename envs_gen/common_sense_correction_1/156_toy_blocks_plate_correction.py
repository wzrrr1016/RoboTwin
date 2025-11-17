from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 156_toy_blocks_plate_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        
        # Add target objects (solid toy blocks and markpen)
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.markpen = self.add_actor("markpen", "markpen")
        
        # Add distractors
        distractor_list = ["alarm-clock", "dumbbell", "tissue-box", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # 1. Pick red_block and place it onto plate
        success = self.pick_and_place(self.red_block, self.plate)
        print("Pick red_block:", success)
        if not success:
            return self.info

        # 2. Pick markpen and place it onto plate (wrong action)
        success = self.pick_and_place(self.markpen, self.plate)
        print("Pick markpen (wrong):", success)
        if not success:
            return self.info

        # 3. Pick markpen from plate and place it onto table (recovery)
        success = self.pick_and_place(self.markpen, self.table)
        print("Recover markpen:", success)
        if not success:
            return self.info

        # 4. Pick green_block and place it onto plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("Pick green_block:", success)
        if not success:
            return self.info

        # 5. Pick blue_block and place it onto plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Pick blue_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all required blocks are on the plate"""
        return (
            self.check_on(self.red_block, self.plate) and
            self.check_on(self.green_block, self.plate) and
            self.check_on(self.blue_block, self.plate)
        )
