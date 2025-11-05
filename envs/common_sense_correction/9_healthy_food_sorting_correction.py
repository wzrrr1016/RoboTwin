from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_sorting_correction_9(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.fork = self.add_actor("fork", "fork")
        self.scanner = self.add_actor("scanner", "scanner")

    def play_once(self):
        # Place apple into plate
        success = self.pick_and_place(self.apple, self.plate)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Place fork into plate
        success = self.pick_and_place(self.fork, self.plate)
        print("pick place fork:", success)
        if not success:
            return self.info

        # Place scanner into wooden box
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("pick place scanner:", success)
        if not success:
            return self.info

        # Place hamburg into wooden box
        success = self.pick_and_place(self.hamburg, self.wooden_box)
        print("pick place hamburg:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if apple and fork are on the plate
        if not (self.check_on(self.apple, self.plate) and self.check_on(self.fork, self.plate)):
            return False

        # Check if scanner and hamburg are on the wooden box
        if not (self.check_on(self.scanner, self.wooden_box) and self.check_on(self.hamburg, self.wooden_box)):
            return False

        return True
