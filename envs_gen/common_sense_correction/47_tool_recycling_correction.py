from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 47_tool_recycling_correction(Imagine_Task):
    def load_actors(self):
        # Load the dustbin as a container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Load the tool items and other objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

    def play_once(self):
        # Step 1: Pick hammer and place into dustbin (correct action)
        success = self.pick_and_place(self.hammer, self.dustbin)
        print("pick place hammer:", success)
        if not success:
            return self.info

        # Step 2: Pick alarm-clock and place into dustbin (wrong action)
        success = self.pick_and_place(self.alarm_clock, self.dustbin)
        print("pick place alarm-clock:", success)
        if not success:
            return self.info

        # Step 3: Pick alarm-clock from dustbin and place on table (recovery)
        success = self.pick_and_place(self.alarm_clock, self.table)
        print("pick place alarm-clock on table:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the hammer is in the dustbin (correct action)
        if not self.check_on(self.hammer, self.dustbin):
            return False
        # Check if the alarm-clock is on the table (recovery action)
        if not self.check_on(self.alarm_clock, self.table):
            return False
        return True
