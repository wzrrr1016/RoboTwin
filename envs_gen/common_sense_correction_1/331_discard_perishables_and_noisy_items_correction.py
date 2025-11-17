from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 331_discard_perishables_and_noisy_items_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        Adds the dustbin, target objects (apple, alarm-clock, mug, stapler), 
        and distractors as specified in the task description.
        """
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add target objects
        self.apple = self.add_actor("apple", "apple")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.mug = self.add_actor("mug", "mug")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractors
        distractor_list = ["pet-collar", "roll-paper", "red_block", "blue_block", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Pick alarm-clock and place into dustbin (correct action)
        2. Pick mug and place into dustbin (wrong action)
        3. Pick mug from dustbin and place on table (recovery action)
        4. Pick apple and place into dustbin (correct action)
        5. Pick stapler and place on table (correct action)
        """
        # Step 1: Pick alarm-clock and place into dustbin
        success = self.pick_and_place(self.alarm_clock, self.dustbin)
        print("Pick alarm-clock into dustbin:", success)
        if not success:
            return self.info

        # Step 2: Pick mug and place into dustbin (wrong action)
        success = self.pick_and_place(self.mug, self.dustbin)
        print("Pick mug into dustbin (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick mug from dustbin and place on table (recovery)
        success = self.pick_and_place(self.mug, self.table)
        print("Recover mug to table:", success)
        if not success:
            return self.info

        # Step 4: Pick apple and place into dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Pick apple into dustbin:", success)
        if not success:
            return self.info

        # Step 5: Pick stapler and place on table
        success = self.pick_and_place(self.stapler, self.table)
        print("Place stapler on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Perishable food (apple) and noisy item (alarm-clock) are in the dustbin
        - Mug is not in the dustbin (recovered)
        - Stapler is on the table
        """
        # Check if alarm-clock is in the dustbin
        alarm_in_dustbin = self.check_on(self.alarm_clock, self.dustbin)
        
        # Check if apple is in the dustbin
        apple_in_dustbin = self.check_on(self.apple, self.dustbin)
        
        # Check if mug is not in the dustbin
        mug_not_in_dustbin = not self.check_on(self.mug, self.dustbin)
        
        # Check if stapler is on the table
        stapler_on_table = self.check_on(self.stapler, self.table)

        # Return True only if all conditions are met
        return alarm_in_dustbin and apple_in_dustbin and mug_not_in_dustbin and stapler_on_table
