from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 29_timekeeping_device_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.microphone = self.add_actor("microphone", "microphone")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.book = self.add_actor("book", "book")

    def play_once(self):
        # Pick alarm-clock and place into plate
        success = self.pick_and_place(self.alarm_clock, self.plate)
        print("pick place alarm-clock:", success)
        if not success:
            return self.info
        
        # Pick microphone and place into wooden_box
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("pick place microphone:", success)
        if not success:
            return self.info
        
        # Pick sand-clock and place into plate
        success = self.pick_and_place(self.sand_clock, self.plate)
        print("pick place sand-clock:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if alarm-clock is on plate
        if not self.check_on(self.alarm_clock, self.plate):
            return False
        
        # Check if microphone is on wooden_box
        if not self.check_on(self.microphone, self.wooden_box):
            return False
        
        # Check if sand-clock is on plate
        if not self.check_on(self.sand_clock, self.plate):
            return False
        
        return True
