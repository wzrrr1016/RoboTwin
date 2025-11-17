from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 65_store_perishables_keep_electronics_outside_correction(Imagine_Task):
    def load_actors(self):
        # Add the wooden box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add perishable food items
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add small electronic devices
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.microphone = self.add_actor("microphone", "microphone")
        
        # Add distractors
        distractor_list = ["shoe", "book", "pot-with-plant", "dumbbell", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place perishable food items into the wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Pick and place apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hamburg, self.wooden_box)
        print("Pick and place hamburg:", success)
        if not success:
            return self.info

        # Place small electronic devices on top of the wooden_box
        success = self.pick_and_place(self.alarm_clock, self.wooden_box)
        print("Pick and place alarm-clock:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("Pick and place microphone:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all required objects are placed correctly
        if (self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.hamburg, self.wooden_box) and
            self.check_on(self.alarm_clock, self.wooden_box) and
            self.check_on(self.microphone, self.wooden_box)):
            return True
        return False
