from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 46_healthy_food_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")

        # Load objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")

    def play_once(self):
        # Step 1: Pick apple and place into coaster (wrong)
        success = self.pick_and_place(self.apple, self.coaster)
        print("pick place apple into coaster:", success)
        if not success:
            return self.info

        # Step 2: Pick apple from coaster and place into plate (correct)
        success = self.pick_and_place(self.apple, self.plate)
        print("pick place apple into plate:", success)
        if not success:
            return self.info

        # Step 3: Pick bread and place into plate (correct)
        success = self.pick_and_place(self.bread, self.plate)
        print("pick place bread into plate:", success)
        if not success:
            return self.info

        # Step 4: Pick french fries and place into coaster (correct)
        success = self.pick_and_place(self.french_fries, self.coaster)
        print("pick place french fries into coaster:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if apple is on plate
        apple_on_plate = self.check_on(self.apple, self.plate)
        # Check if bread is on plate
        bread_on_plate = self.check_on(self.bread, self.plate)
        # Check if french fries is on coaster
        fries_on_coaster = self.check_on(self.french_fries, self.coaster)

        return apple_on_plate and bread_on_plate and fries_on_coaster
