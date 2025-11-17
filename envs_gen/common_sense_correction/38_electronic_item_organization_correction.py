from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 38_electronic_item_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.can = self.add_actor("can", "can")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors
        distractor_list = ['pet-collar', 'table-tennis', 'roll-paper', 'baguette', 'apple']
        self.add_distractors(distractor_list)

        self.check_scene()

    def play_once(self):
        # Step 1: Pick alarm-clock and place into tray
        success = self.pick_and_place(self.alarm_clock, self.tray)
        print("Place alarm clock:", success)
        if not success:
            return self.info

        # Step 2: Pick small-speaker and place into tray
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Place small speaker:", success)
        if not success:
            return self.info

        # Step 3: Pick can and place into tray (wrong)
        success = self.pick_and_place(self.can, self.tray)
        print("Place can (wrong):", success)
        if not success:
            return self.info

        # Step 4: Pick can from tray and place into dustbin (recovery)
        success = self.pick_and_place(self.can, self.dustbin)
        print("Move can to dustbin:", success)
        if not success:
            return self.info

        # Step 5: Pick cup_without_handle and place into dustbin
        success = self.pick_and_place(self.cup_without_handle, self.dustbin)
        print("Place cup without handle:", success)
        if not success:
            return self.info

        # Step 6: Pick screwdriver and place into dustbin
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Check if electronic items are in the tray
        if not (self.check_on(self.alarm_clock, self.tray) and self.check_on(self.small_speaker, self.tray)):
            return False

        # Check if non-electronic items are in the dustbin
        if not (self.check_on(self.can, self.dustbin) and
                self.check_on(self.cup_without_handle, self.dustbin) and
                self.check_on(self.screwdriver, self.dustbin)):
            return False

        return True
