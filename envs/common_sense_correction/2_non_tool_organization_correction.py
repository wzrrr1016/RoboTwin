from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class non_tool_organization_correction_2(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the non-tool items to be placed
        self.microphone = self.add_actor("microphone", "microphone")
        self.mouse = self.add_actor("mouse", "mouse")
        self.toycar = self.add_actor("toycar", "toycar")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add the tool items (not placed)
        self.stapler = self.add_actor("stapler", "stapler")
        self.drill = self.add_actor("drill", "drill")

    def play_once(self):
        # Pick and place each non-tool item into the fluted_block
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("pick place microphone:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mouse, self.fluted_block)
        print("pick place mouse:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("pick place toycar:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("pick place bottle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all non-tool items are on the fluted_block
        if (self.check_on(self.microphone, self.fluted_block) and
            self.check_on(self.mouse, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block)):
            return True
        return False
