from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 31_healthy_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Load the objects
        self.apple = self.add_actor("apple", "apple")
        self.hammer = self.add_actor("hammer", "hammer")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")

    def play_once(self):
        # Pick apple and place it into the tray
        success = self.pick_and_place(self.apple, self.tray)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Pick hammer and place it into the fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("pick place hammer:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if apple is on the tray and hammer is on the fluted_block
        if self.check_on(self.apple, self.tray) and self.check_on(self.hammer, self.fluted_block):
            return True
        return False
