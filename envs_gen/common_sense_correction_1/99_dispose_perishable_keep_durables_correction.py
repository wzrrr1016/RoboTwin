from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 99_dispose_perishable_keep_durables_correction(Imagine_Task):
    def load_actors(self):
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractors
        distractor_list = ['toycar', 'green_block', 'blue_block', 'yellow_block', 'purple_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick apple and place into dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Pick apple:", success)
        if not success:
            return self.info

        # 2. Pick alarm-clock and place into dustbin (wrong action)
        success = self.pick_and_place(self.alarm_clock, self.dustbin)
        print("Pick alarm-clock (wrong):", success)
        if not success:
            return self.info

        # 3. Pick alarm-clock from dustbin and place on table (recovery)
        success = self.pick_and_place(self.alarm_clock, self.table)
        print("Recover alarm-clock:", success)
        if not success:
            return self.info

        # 4. Pick french_fries and place into dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Pick french fries:", success)
        if not success:
            return self.info

        # 5. Pick hammer and place on table (should not be discarded)
        success = self.pick_and_place(self.hammer, self.table)
        print("Pick hammer:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if perishable/oily foods are in dustbin
        apple_in = self.check_on(self.apple, self.dustbin)
        fries_in = self.check_on(self.french_fries, self.dustbin)
        
        # Check if durable items are NOT in dustbin
        alarm_not_in = not self.check_on(self.alarm_clock, self.dustbin)
        hammer_not_in = not self.check_on(self.hammer, self.dustbin)
        
        return apple_in and fries_in and alarm_not_in and hammer_not_in
