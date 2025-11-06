from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 45_tool_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.mug = self.add_actor("mug", "mug")
        self.drill = self.add_actor("drill", "drill")

    def play_once(self):
        # Step 1: Pick hammer and place into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("pick place hammer:", success)
        if not success:
            return self.info

        # Step 2: Pick dumbbell and place into wooden_box (wrong)
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("pick place dumbbell:", success)
        if not success:
            return self.info

        # Step 3: Pick dumbbell from wooden_box and place into coaster
        success = self.pick_and_place(self.dumbbell, self.coaster)
        print("pick place dumbbell to coaster:", success)
        if not success:
            return self.info

        # Step 4: Pick sand-clock and place into coaster
        success = self.pick_and_place(self.sand_clock, self.coaster)
        print("pick place sand-clock:", success)
        if not success:
            return self.info

        # Step 5: Pick mug and place into coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("pick place mug:", success)
        if not success:
            return self.info

        # Step 6: Pick drill and place into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("pick place drill:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check hammer is in wooden_box
        if not self.check_on(self.hammer, self.wooden_box):
            return False
        # Check dumbbell is in coaster
        if not self.check_on(self.dumbbell, self.coaster):
            return False
        # Check sand-clock is in coaster
        if not self.check_on(self.sand_clock, self.coaster):
            return False
        # Check mug is in coaster
        if not self.check_on(self.mug, self.coaster):
            return False
        # Check drill is in wooden_box
        if not self.check_on(self.drill, self.wooden_box):
            return False
        return True
