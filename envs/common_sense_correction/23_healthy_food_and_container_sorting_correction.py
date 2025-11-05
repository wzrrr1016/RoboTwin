from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_and_container_sorting_correction_23(Imagine_Task):
    def load_actors(self):
        # Load all required actors
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.can = self.add_actor("can", "can")
        self.scanner = self.add_actor("scanner", "scanner")
        self.toycar = self.add_actor("toycar", "toycar")

    def play_once(self):
        # Pick apple and place into plate
        success = self.pick_and_place(self.apple, self.plate)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Pick can and place into tray
        success = self.pick_and_place(self.can, self.tray)
        print("pick place can:", success)
        if not success:
            return self.info

        # Pick scanner and place into tray
        success = self.pick_and_place(self.scanner, self.tray)
        print("pick place scanner:", success)
        if not success:
            return self.info

        # Pick hamburg and place into tray
        success = self.pick_and_place(self.hamburg, self.tray)
        print("pick place hamburg:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if apple is on the plate
        if not self.check_on(self.apple, self.plate):
            return False

        # Check if can is on the tray
        if not self.check_on(self.can, self.tray):
            return False

        # Check if scanner is on the tray
        if not self.check_on(self.scanner, self.tray):
            return False

        # Check if hamburg is on the tray (as per the task instruction)
        if not self.check_on(self.hamburg, self.tray):
            return False

        return True
