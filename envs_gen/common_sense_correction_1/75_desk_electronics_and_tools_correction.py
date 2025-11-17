from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 75_desk_electronics_and_tools_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create required objects
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.mouse = self.add_actor("mouse", "mouse")
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractors
        distractor_list = ["apple", "baguette", "chips-tub", "red_block", "blue_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place alarm-clock on coaster
        success = self.pick_and_place(self.alarm_clock, self.coaster)
        print("Place alarm-clock on coaster:", success)
        if not success:
            return self.info

        # Wrongly place hammer on coaster
        success = self.pick_and_place(self.hammer, self.coaster)
        print("Place hammer on coaster (wrong):", success)
        if not success:
            return self.info

        # Recovery: move hammer to shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Move hammer to shoe_box:", success)
        if not success:
            return self.info

        # Place drill in shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Place drill in shoe_box:", success)
        if not success:
            return self.info

        # Place mouse on coaster
        success = self.pick_and_place(self.mouse, self.coaster)
        print("Place mouse on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check small electronic items on coaster
        if not (self.check_on(self.alarm_clock, self.coaster) and 
                self.check_on(self.mouse, self.coaster)):
            return False
        
        # Check heavier repair tools in shoe_box
        if not (self.check_on(self.hammer, self.shoe_box) and 
                self.check_on(self.drill, self.shoe_box)):
            return False
        
        return True
