from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 22_tool_organization_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Load objects
        self.drill = self.add_actor("drill", "drill")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.fork = self.add_actor("fork", "fork")
        self.mouse = self.add_actor("mouse", "mouse")
        self.toycar = self.add_actor("toycar", "toycar")

    def play_once(self):
        # Step 1: Pick drill and place into fluted_block (wrong step)
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("pick place drill into fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Pick drill from fluted_block and place into dustbin (correct step)
        success = self.pick_and_place(self.drill, self.dustbin)
        print("pick place drill into dustbin:", success)
        if not success:
            return self.info

        # Step 3: Pick dumbbell and place into dustbin
        success = self.pick_and_place(self.dumbbell, self.dustbin)
        print("pick place dumbbell into dustbin:", success)
        if not success:
            return self.info

        # Step 4: Pick fork and place into dustbin
        success = self.pick_and_place(self.fork, self.dustbin)
        print("pick place fork into dustbin:", success)
        if not success:
            return self.info

        # Step 5: Pick mouse and place into dustbin
        success = self.pick_and_place(self.mouse, self.dustbin)
        print("pick place mouse into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if drill is in dustbin (corrected step)
        if not self.check_on(self.drill, self.dustbin):
            return False

        # Check if all non-power tools are in dustbin
        if not self.check_on(self.dumbbell, self.dustbin):
            return False
        if not self.check_on(self.fork, self.dustbin):
            return False
        if not self.check_on(self.mouse, self.dustbin):
            return False

        # Ensure toycar is also in dustbin
        if not self.check_on(self.toycar, self.dustbin):
            return False

        return True
