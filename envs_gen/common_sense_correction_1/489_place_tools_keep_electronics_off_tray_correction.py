from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 489_place_tools_keep_electronics_off_tray_correction(Imagine_Task):
    def load_actors(self):
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        # Add the required objects
        self.stapler = self.add_actor("stapler", "stapler")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.scanner = self.add_actor("scanner", "scanner")
        # Add distractors
        distractor_list = ['chips-tub', 'jam-jar', 'pet-collar', 'red_block', 'tissue-box']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place alarm-clock on tray (wrong action)
        success = self.pick_and_place(self.alarm_clock, self.tray)
        print("Place alarm-clock on tray:", success)
        if not success:
            return self.info

        # Step 2: Recovery - Move alarm-clock back to table
        success = self.pick_and_place(self.alarm_clock, self.table)
        print("Move alarm-clock back to table:", success)
        if not success:
            return self.info

        # Step 3: Place stapler on tray
        success = self.pick_and_place(self.stapler, self.tray)
        print("Place stapler on tray:", success)
        if not success:
            return self.info

        # Step 4: Place screwdriver on tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Place screwdriver on tray:", success)
        if not success:
            return self.info

        # Step 5: Place scanner on table
        success = self.pick_and_place(self.scanner, self.table)
        print("Place scanner on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if stapler and screwdriver are on the tray
        stapler_on_tray = self.check_on(self.stapler, self.tray)
        screwdriver_on_tray = self.check_on(self.screwdriver, self.tray)

        # Check if alarm-clock and scanner are NOT on the tray
        alarm_clock_not_on_tray = not self.check_on(self.alarm_clock, self.tray)
        scanner_not_on_tray = not self.check_on(self.scanner, self.tray)

        # Return True only if all conditions are met
        return stapler_on_tray and screwdriver_on_tray and alarm_clock_not_on_tray and scanner_not_on_tray
