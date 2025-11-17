from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 430_dining_items_and_tools_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        
        # Create objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.cup = self.add_actor("cup", "cup")
        
        # Add distractors
        distractors = ['toycar', 'pot-with-plant', 'alarm-clock', 'shoe', 'book']
        self.add_distractors(distractors)

    def play_once(self):
        # Wrong action: place screwdriver into plate
        success = self.pick_and_place(self.screwdriver, self.plate)
        print("Place screwdriver into plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: place screwdriver into tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Place screwdriver into tray (recovery):", success)
        if not success:
            return self.info

        # Place dining items into plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Place fork into plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.knife, self.plate)
        print("Place knife into plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup, self.plate)
        print("Place cup into plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all dining items are on plate and tool is on tray
        if (self.check_on(self.fork, self.plate) and
            self.check_on(self.knife, self.plate) and
            self.check_on(self.cup, self.plate) and
            self.check_on(self.screwdriver, self.tray)):
            return True
        return False
