from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 291_office_electronics_on_tray_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        # Add small electronic office accessories
        self.mouse = self.add_actor("mouse", "mouse")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        # Add metal binding tool (should be excluded from tray)
        self.stapler = self.add_actor("stapler", "stapler")
        # Add distractor objects
        distractors = ["baguette", "pot-with-plant", "shoe", "toycar", "apple"]
        self.add_distractors(distractors)

    def play_once(self):
        # 1. Pick mouse and place on tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("Place mouse:", success)
        if not success:
            return self.info

        # 2. Pick stapler and place on tray (wrong action)
        success = self.pick_and_place(self.stapler, self.tray)
        print("Place stapler (wrong):", success)
        if not success:
            return self.info

        # 3. Pick stapler from tray and place on mouse (recovery)
        success = self.pick_and_place(self.stapler, self.mouse)
        print("Recover stapler:", success)
        if not success:
            return self.info

        # 4. Pick alarm-clock and place on tray
        success = self.pick_and_place(self.alarm_clock, self.tray)
        print("Place alarm-clock:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if small electronics are on tray and metal tool is not
        mouse_on_tray = self.check_on(self.mouse, self.tray)
        alarm_on_tray = self.check_on(self.alarm_clock, self.tray)
        stapler_not_on_tray = not self.check_on(self.stapler, self.tray)
        
        return mouse_on_tray and alarm_on_tray and stapler_not_on_tray
```
