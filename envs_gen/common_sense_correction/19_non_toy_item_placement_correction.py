from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 19_non_toy_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the wooden_box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the non-toy items
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.drill = self.add_actor("drill", "drill")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.hamburg = self.add_actor("hamburg", "hamburg")

    def play_once(self):
        # Pick and place alarm-clock into wooden_box
        success = self.pick_and_place(self.alarm_clock, self.wooden_box)
        print("pick place alarm-clock:", success)
        if not success:
            return self.info

        # Pick and place drill into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("pick place drill:", success)
        if not success:
            return self.info

        # Pick and place dumbbell into wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("pick place dumbbell:", success)
        if not success:
            return self.info

        # Pick and place hamburg into wooden_box
        success = self.pick_and_place(self.hamburg, self.wooden_box)
        print("pick place hamburg:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all non-toy items are on the wooden_box
        if (self.check_on(self.alarm_clock, self.wooden_box) and
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.dumbbell, self.wooden_box) and
            self.check_on(self.hamburg, self.wooden_box)):
            return True
        return False
