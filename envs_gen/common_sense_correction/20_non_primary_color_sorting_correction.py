from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 20_non_primary_color_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add the dustbin as a container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add the non-primary color items
        self.hammer = self.add_actor("hammer", "hammer")
        self.toycar = self.add_actor("toycar", "toycar")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.green_block = self.add_actor("green_block", "green_block")

    def play_once(self):
        # Pick and place each non-primary item into the dustbin
        success = self.pick_and_place(self.hammer, self.dustbin)
        print("pick place hammer:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.toycar, self.dustbin)
        print("pick place toycar:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.sand_clock, self.dustbin)
        print("pick place sand-clock:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.pot_with_plant, self.dustbin)
        print("pick place pot-with-plant:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.dustbin)
        print("pick place green_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all non-primary items are on the dustbin
        if (self.check_on(self.hammer, self.dustbin) and
            self.check_on(self.toycar, self.dustbin) and
            self.check_on(self.sand_clock, self.dustbin) and
            self.check_on(self.pot_with_plant, self.dustbin) and
            self.check_on(self.green_block, self.dustbin)):
            return True
        return False
