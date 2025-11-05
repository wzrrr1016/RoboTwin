from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 14_timekeeping_device_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.plate = self.add_actor("plate", "plate")

        # Add objects
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.bread = self.add_actor("bread", "bread")

    def play_once(self):
        # Step 1: Pick sand-clock and place into coaster (wrong)
        success = self.pick_and_place(self.sand_clock, self.coaster)
        print("pick place sand_clock into coaster:", success)
        if not success:
            return self.info

        # Step 2: Pick sand-clock from coaster and place into plate (correct)
        success = self.pick_and_place(self.sand_clock, self.plate)
        print("pick place sand_clock into plate:", success)
        if not success:
            return self.info

        # Step 3: Pick alarm-clock and place into coaster
        success = self.pick_and_place(self.alarm_clock, self.coaster)
        print("pick place alarm_clock into coaster:", success)
        if not success:
            return self.info

        # Step 4: Place yellow_block on plate
        success = self.pick_and_place(self.yellow_block, self.plate)
        print("pick place yellow_block into plate:", success)
        if not success:
            return self.info

        # Step 5: Place purple_block on plate
        success = self.pick_and_place(self.purple_block, self.plate)
        print("pick place purple_block into plate:", success)
        if not success:
            return self.info

        # Step 6: Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("pick place bread into plate:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if alarm_clock is in coaster
        if not self.check_on(self.alarm_clock, self.coaster):
            return False

        # Check if sand_clock is on plate
        if not self.check_on(self.sand_clock, self.plate):
            return False

        # Check if yellow_block is on plate
        if not self.check_on(self.yellow_block, self.plate):
            return False

        # Check if purple_block is on plate
        if not self.check_on(self.purple_block, self.plate):
            return False

        # Check if bread is on plate
        if not self.check_on(self.bread, self.plate):
            return False

        return True
