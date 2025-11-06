from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 13_tool_storage_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.table = self.add_actor("table", "table")

        # Load objects
        self.drill = self.add_actor("drill", "drill")
        self.hammer = self.add_actor("hammer", "hammer")
        self.mouse = self.add_actor("mouse", "mouse")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.bottle = self.add_actor("bottle", "bottle")

    def play_once(self):
        # Place drill (power tool) into shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("pick place drill into shoe_box:", success)
        if not success:
            return self.info

        # Place hammer (power tool) into shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("pick place hammer into shoe_box:", success)
        if not success:
            return self.info

        # Place mouse (electronic device) onto table
        success = self.pick_and_place(self.mouse, self.table)
        print("pick place mouse into table:", success)
        if not success:
            return self.info

        # Place alarm-clock (electronic device) onto table
        success = self.pick_and_place(self.alarm_clock, self.table)
        print("pick place alarm-clock into table:", success)
        if not success:
            return self.info

        # Place tissue-box into shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("pick place tissue-box into shoe_box:", success)
        if not success:
            return self.info

        # Place bottle into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("pick place bottle into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check power tools (drill, hammer) are in shoe_box
        if self.check_on(self.drill, self.shoe_box) and self.check_on(self.hammer, self.shoe_box):
            # Check electronic devices (mouse, alarm-clock) are on table
            if self.check_on(self.mouse, self.table) and self.check_on(self.alarm_clock, self.table):
                # Check other items (tissue-box, bottle) are in shoe_box
                if self.check_on(self.tissue_box, self.shoe_box) and self.check_on(self.bottle, self.shoe_box):
                    return True
        return False
