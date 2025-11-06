from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 28_non_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Load objects
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.fork = self.add_actor("fork", "fork")

    def play_once(self):
        # Step 1: Place alarm-clock into wooden_box
        success = self.pick_and_place(self.alarm_clock, self.wooden_box)
        print("pick place alarm-clock:", success)
        if not success:
            return self.info

        # Step 2: Place pot-with-plant into wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("pick place pot-with-plant:", success)
        if not success:
            return self.info

        # Step 3: Place fork into wooden_box (wrong step, to be recovered)
        success = self.pick_and_place(self.fork, self.wooden_box)
        print("pick place fork:", success)
        if not success:
            return self.info

        # Step 4: Recover fork from wooden_box and place on table
        success = self.pick_and_place(self.fork, self.table)
        print("pick place fork on table:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if alarm-clock is on wooden_box
        if not self.check_on(self.alarm_clock, self.wooden_box):
            return False
        # Check if pot-with-plant is on wooden_box
        if not self.check_on(self.pot_with_plant, self.wooden_box):
            return False
        # Check if fork is on table
        if not self.check_on(self.fork, self.table):
            return False
        return True
