from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 26_electronics_on_tray_sharp_off_correction(Imagine_Task):
    def load_actors(self):
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Add required objects
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.mouse = self.add_actor("mouse", "mouse")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractor objects
        distractor_list = ['chips-tub', 'pet-collar', 'dumbbell', 'roll-paper', 'shampoo']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: Place knife on tray (needs recovery)
        success = self.pick_and_place(self.knife, self.tray)
        print("Pick knife and place on tray (wrong):", success)
        if not success:
            return self.info

        # Recovery: Pick knife from tray and place on table
        success = self.pick_and_place(self.knife, self.table)
        print("Pick knife from tray and place on table (recovery):", success)
        if not success:
            return self.info

        # Place small electronic devices on tray
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Pick small-speaker and place on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.alarm_clock, self.tray)
        print("Pick alarm-clock and place on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mouse, self.tray)
        print("Pick mouse and place on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all small electronic devices are on the tray
        # and knife is not on the tray
        if (
            self.check_on(self.small_speaker, self.tray) and
            self.check_on(self.alarm_clock, self.tray) and
            self.check_on(self.mouse, self.tray) and
            not self.check_on(self.knife, self.tray)
        ):
            return True
        return False
