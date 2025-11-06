from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 12_toy_and_non_toy_grouping_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.mouse = self.add_actor("mouse", "mouse")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

    def play_once(self):
        # Step 1: Place toycar into fluted_block (correct)
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("pick place toycar:", success)
        if not success:
            return self.info

        # Step 2: Place sand-clock into fluted_block (wrong)
        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("pick place sand-clock:", success)
        if not success:
            return self.info

        # Step 3: Move sand-clock from fluted_block to wooden_box (recovery)
        success = self.pick_and_place(self.sand_clock, self.wooden_box)
        print("pick place sand-clock to wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place mouse into wooden_box (correct)
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("pick place mouse:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell into wooden_box (correct)
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("pick place dumbbell:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check toycar is in fluted_block
        if not self.check_on(self.toycar, self.fluted_block):
            return False
        # Check sand-clock is in wooden_box
        if not self.check_on(self.sand_clock, self.wooden_box):
            return False
        # Check mouse is in wooden_box
        if not self.check_on(self.mouse, self.wooden_box):
            return False
        # Check dumbbell is in wooden_box
        if not self.check_on(self.dumbbell, self.wooden_box):
            return False
        return True
