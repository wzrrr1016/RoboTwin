from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 335_place_perishable_foods_on_coaster_with_correction(Imagine_Task):
    def load_actors(self):
        # Load the required actors into the environment
        self.coaster = self.add_actor("coaster", "coaster")
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.red_block = self.add_actor("red_block", "red_block")
        self.stapler = self.add_actor("stapler", "stapler")

        # Add distractor objects to the environment
        distractor_list = [
            "pot-with-plant", "alarm-clock", "dumbbell", "shoe", "microphone"
        ]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrong action - pick stapler and place on coaster
        success = self.pick_and_place(self.stapler, self.coaster)
        print("Wrong action - stapler to coaster:", success)
        if not success:
            return self.info

        # Step 2: Recovery - pick stapler from coaster and place on table
        success = self.pick_and_place(self.stapler, self.table)
        print("Recovery - stapler to table:", success)
        if not success:
            return self.info

        # Step 3: Pick apple and place on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Apple to coaster:", success)
        if not success:
            return self.info

        # Step 4: Pick french fries and place on coaster
        success = self.pick_and_place(self.french_fries, self.coaster)
        print("French fries to coaster:", success)
        if not success:
            return self.info

        # Step 5: Pick red_block and place on table
        success = self.pick_and_place(self.red_block, self.table)
        print("Red block to table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required conditions are met
        apple_on_coaster = self.check_on(self.apple, self.coaster)
        french_fries_on_coaster = self.check_on(self.french_fries, self.coaster)
        stapler_on_table = self.check_on(self.stapler, self.table)
        red_block_on_table = self.check_on(self.red_block, self.table)

        return (
            apple_on_coaster
            and french_fries_on_coaster
            and stapler_on_table
            and red_block_on_table
        )
