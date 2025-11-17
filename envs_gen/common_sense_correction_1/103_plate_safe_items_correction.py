from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 103_plate_safe_items_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment."""
        self.plate = self.add_actor("plate", "plate")
        self.stapler = self.add_actor("stapler", "stapler")
        self.red_block = self.add_actor("red_block", "red_block")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        distractor_list = ["pot-with-plant", "shoe", "pet-collar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions for the task."""
        # Wrong action: place dumbbell on plate
        success = self.pick_and_place(self.dumbbell, self.plate)
        print("Pick dumbbell and place on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: place dumbbell back on table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick dumbbell from plate and place on table (recovery):", success)
        if not success:
            return self.info

        # Correct actions
        success = self.pick_and_place(self.stapler, self.plate)
        print("Pick stapler and place on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.red_block, self.plate)
        print("Pick red_block and place on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Pick cup_with_handle and place on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        if (self.check_on(self.stapler, self.plate) and
            self.check_on(self.red_block, self.plate) and
            self.check_on(self.cup_with_handle, self.plate) and
            not self.check_on(self.dumbbell, self.plate)):
            return True
        return False
