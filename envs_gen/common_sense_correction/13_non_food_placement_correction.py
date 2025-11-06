from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 13_non_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the plate (container) and the objects
        self.plate = self.add_actor("plate", "plate")
        self.scanner = self.add_actor("scanner", "scanner")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.bottle = self.add_actor("bottle", "bottle")
        self.drill = self.add_actor("drill", "drill")

    def play_once(self):
        # Step 1: Place non-food items into the plate
        success = self.pick_and_place(self.scanner, self.plate)
        print("pick place scanner:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.sand_clock, self.plate)
        print("pick place sand-clock:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.drill, self.plate)
        print("pick place drill:", success)
        if not success:
            return self.info

        # Step 2: Place the bottle into the plate (wrong)
        success = self.pick_and_place(self.bottle, self.plate)
        print("pick place bottle (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover the bottle from the plate to the table
        success = self.pick_and_place(self.bottle, self.table)
        print("pick place bottle to table:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if non-food items are on the plate
        if (self.check_on(self.scanner, self.plate) and
            self.check_on(self.sand_clock, self.plate) and
            self.check_on(self.drill, self.plate)):

            # Check if the bottle is on the table (recovered)
            if self.check_on(self.bottle, self.table):
                return True

        return False
