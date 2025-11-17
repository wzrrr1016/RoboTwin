from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 455_organize_kitchen_drink_vs_electronics_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add required objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.fork = self.add_actor("fork", "fork")
        self.bottle = self.add_actor("bottle", "bottle")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.scanner = self.add_actor("scanner", "scanner")

        # Add distractors
        distractors = ["toycar", "shoe", "pet-collar", "book", "dumbbell"]
        self.add_distractors(distractors)

    def play_once(self):
        # Place cup_with_handle on tray
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Pick cup_with_handle and place on tray:", success)
        if not success:
            return self.info

        # Place fork on tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick fork and place on tray:", success)
        if not success:
            return self.info

        # Wrongly place alarm-clock on tray
        success = self.pick_and_place(self.alarm_clock, self.tray)
        print("Pick alarm-clock and place on tray (wrong):", success)
        if not success:
            return self.info

        # Correct by placing alarm-clock into dustbin
        success = self.pick_and_place(self.alarm_clock, self.dustbin)
        print("Pick alarm-clock from tray and place into dustbin (recovery):", success)
        if not success:
            return self.info

        # Place scanner into dustbin
        success = self.pick_and_place(self.scanner, self.dustbin)
        print("Pick scanner and place into dustbin:", success)
        if not success:
            return self.info

        # Place bottle on tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("Pick bottle and place on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all non-electronic kitchen and drink items are on the tray
        # and all electronic devices are in the dustbin
        if (
            self.check_on(self.cup_with_handle, self.tray) and
            self.check_on(self.fork, self.tray) and
            self.check_on(self.bottle, self.tray) and
            self.check_on(self.alarm_clock, self.dustbin) and
            self.check_on(self.scanner, self.dustbin)
        ):
            return True
        return False
