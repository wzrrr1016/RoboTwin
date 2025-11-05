from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 18_timekeeping_device_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bottle = self.add_actor("bottle", "bottle")

    def play_once(self):
        # Pick sand-clock and place into wooden_box
        success = self.pick_and_place(self.sand_clock, self.wooden_box)
        print("pick place sand_clock:", success)
        if not success:
            return self.info

        # Pick alarm-clock and place into wooden_box
        success = self.pick_and_place(self.alarm_clock, self.wooden_box)
        print("pick place alarm_clock:", success)
        if not success:
            return self.info

        # Pick cup_without_handle and place into shoe_box
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("pick place cup_without_handle:", success)
        if not success:
            return self.info

        # Pick tissue-box and place into shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("pick place tissue_box:", success)
        if not success:
            return self.info

        # Pick bottle and place into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("pick place bottle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if timekeeping devices are in wooden_box
        if not (self.check_on(self.sand_clock, self.wooden_box) and 
                self.check_on(self.alarm_clock, self.wooden_box)):
            return False

        # Check if other items are in shoe_box
        if not (self.check_on(self.cup_without_handle, self.shoe_box) and 
                self.check_on(self.tissue_box, self.shoe_box) and 
                self.check_on(self.bottle, self.shoe_box)):
            return False

        return True
