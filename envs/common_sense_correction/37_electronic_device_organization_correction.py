from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class electronic_device_organization_correction_37(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        # Add objects
        self.microphone = self.add_actor("microphone", "microphone")
        self.mouse = self.add_actor("mouse", "mouse")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.toycar = self.add_actor("toycar", "toycar")

    def play_once(self):
        # Step 1: Pick microphone and place into tray
        success = self.pick_and_place(self.microphone, self.tray)
        print("pick place microphone:", success)
        if not success:
            return self.info

        # Step 2: Pick mouse and place into tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("pick place mouse:", success)
        if not success:
            return self.info

        # Step 3: Pick alarm-clock and place into shoe_box (wrong)
        success = self.pick_and_place(self.alarm_clock, self.shoe_box)
        print("pick place alarm-clock into shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Pick alarm-clock from shoe_box and place into tray
        success = self.pick_and_place(self.alarm_clock, self.tray)
        print("pick place alarm-clock into tray:", success)
        if not success:
            return self.info

        # Step 5: Pick dumbbell and place into shoe_box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("pick place dumbbell:", success)
        if not success:
            return self.info

        # Step 6: Pick toycar and place into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("pick place toycar:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all electronic devices (microphone, mouse, alarm-clock) are in the tray
        if (self.check_on(self.microphone, self.tray) and
            self.check_on(self.mouse, self.tray) and
            self.check_on(self.alarm_clock, self.tray)):

            # Check if non-electronic items (dumbbell, toycar) are in the shoe_box
            if (self.check_on(self.dumbbell, self.shoe_box) and
                self.check_on(self.toycar, self.shoe_box)):
                return True

        return False
