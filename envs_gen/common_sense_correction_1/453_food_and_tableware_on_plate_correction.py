from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 453_food_and_tableware_on_plate_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the environment"""
        # Create main actors
        self.plate = self.add_actor("plate", "plate")
        self.apple = self.add_actor("apple", "apple")
        self.mug = self.add_actor("mug", "mug")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractor objects
        distractor_list = ["calculator", "hammer", "alarm-clock", "pot-with-plant", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Initial incorrect action (blue block on plate)
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Place blue_block on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery action (blue block back to table)
        success = self.pick_and_place(self.blue_block, self.table)
        print("Recover blue_block to table:", success)
        if not success:
            return self.info

        # Correct food placement
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mug, self.plate)
        print("Place mug on plate:", success)
        if not success:
            return self.info

        # Block placement (keep off plate)
        success = self.pick_and_place(self.yellow_block, self.table)
        print("Place yellow_block on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check required items on plate
        apple_on_plate = self.check_on(self.apple, self.plate)
        mug_on_plate = self.check_on(self.mug, self.plate)
        
        # Check blocks not on plate
        blue_off_plate = not self.check_on(self.blue_block, self.plate)
        yellow_off_plate = not self.check_on(self.yellow_block, self.plate)
        
        return all([apple_on_plate, mug_on_plate, blue_off_plate, yellow_off_plate])
