from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 5_electronic_device_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add the objects involved in the task
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.microphone = self.add_actor("microphone", "microphone")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")

    def play_once(self):
        # Step 1: Pick alarm-clock from shoe_box and place on table
        success = self.pick_and_place(self.alarm_clock, self.table)
        print("pick place alarm-clock:", success)
        if not success:
            return self.info

        # Step 2: Pick microphone and place into shoe_box
        success = self.pick_and_place(self.microphone, self.shoe_box)
        print("pick place microphone:", success)
        if not success:
            return self.info

        # Step 3: Pick cup_with_handle and place on table
        success = self.pick_and_place(self.cup_with_handle, self.table)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check alarm-clock is on table
        alarm_clock_on_table = self.check_on(self.alarm_clock, self.table)
        # Check microphone is in shoe_box
        microphone_in_shoe_box = self.check_on(self.microphone, self.shoe_box)
        # Check cup_with_handle is on table
        cup_on_table = self.check_on(self.cup_with_handle, self.table)
        return alarm_clock_on_table and microphone_in_shoe_box and cup_on_table
