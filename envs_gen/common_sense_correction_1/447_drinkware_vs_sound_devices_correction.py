from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 447_drinkware_vs_sound_devices_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the objects used in the task
        self.mug = self.add_actor("mug", "mug")
        self.can = self.add_actor("can", "can")
        self.microphone = self.add_actor("microphone", "microphone")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        
        # Add distractors
        distractors = ["shoe", "book", "toycar", "hammer", "apple", "markpen"]
        self.add_distractors(distractors)

    def play_once(self):
        # Step 1: Place mug into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug:", success)
        if not success:
            return self.info

        # Step 2: Place can into fluted_block
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Place can:", success)
        if not success:
            return self.info

        # Step 3: Wrong action - place alarm-clock into fluted_block
        success = self.pick_and_place(self.alarm_clock, self.fluted_block)
        print("Wrong place alarm-clock:", success)
        if not success:
            return self.info

        # Step 4: Recovery - move alarm-clock back to table
        if self.check_on(self.alarm_clock, self.fluted_block):
            success = self.pick_and_place(self.alarm_clock, self.table)
            print("Recover alarm-clock:", success)
            if not success:
                return self.info

        # Step 5: Place microphone on table
        success = self.pick_and_place(self.microphone, self.table)
        print("Place microphone:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if mug and can are on the fluted_block
        mug_on = self.check_on(self.mug, self.fluted_block)
        can_on = self.check_on(self.can, self.fluted_block)

        # Check if alarm-clock and microphone are NOT on the fluted_block
        alarm_off = not self.check_on(self.alarm_clock, self.fluted_block)
        mic_off = not self.check_on(self.microphone, self.fluted_block)

        return mug_on and can_on and alarm_off and mic_off
