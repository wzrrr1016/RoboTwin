from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 24_drinkware_and_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the required containers and objects
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.mug = self.add_actor("mug", "mug")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")

    def play_once(self):
        # Step 1: Pick mug and place into coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("pick place mug:", success)
        if not success:
            return self.info

        # Step 2: Pick alarm-clock and place into coaster (wrong)
        success = self.pick_and_place(self.alarm_clock, self.coaster)
        print("pick place alarm-clock:", success)
        if not success:
            return self.info

        # Step 3: Pick alarm-clock from coaster and place on table (recovery)
        success = self.pick_and_place(self.alarm_clock, self.table)
        print("pick place alarm-clock on table:", success)
        if not success:
            return self.info

        # Step 4: Pick french_fries and place into plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("pick place french_fries:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if mug is on coaster
        if not self.check_on(self.mug, self.coaster):
            return False
        # Check if french_fries is on plate
        if not self.check_on(self.french_fries, self.plate):
            return False
        # Check if alarm-clock is on table
        if not self.check_on(self.alarm_clock, self.table):
            return False
        return True
