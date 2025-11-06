from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 34_food_and_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the required containers and objects
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.drill = self.add_actor("drill", "drill")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.bottle = self.add_actor("bottle", "bottle")

    def play_once(self):
        # Step 1: Pick hamburg and place into plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("pick place hamburg:", success)
        if not success:
            return self.info

        # Step 2: Pick drill and place into plate (wrong action)
        success = self.pick_and_place(self.drill, self.plate)
        print("pick place drill:", success)
        if not success:
            return self.info

        # Step 3: Pick drill from plate and place on table (recovery)
        success = self.pick_and_place(self.drill, self.table)
        print("pick place drill on table:", success)
        if not success:
            return self.info

        # Step 4: Pick sand-clock and place into shoe_box
        success = self.pick_and_place(self.sand_clock, self.shoe_box)
        print("pick place sand-clock:", success)
        if not success:
            return self.info

        # Step 5: Pick bottle and place into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("pick place bottle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if hamburg is on the plate
        if not self.check_on(self.hamburg, self.plate):
            return False

        # Check if sand-clock is on the shoe_box
        if not self.check_on(self.sand_clock, self.shoe_box):
            return False

        # Check if bottle is on the shoe_box
        if not self.check_on(self.bottle, self.shoe_box):
            return False

        # Check if drill is on the table (recovery step)
        if not self.check_on(self.drill, self.table):
            return False

        return True
