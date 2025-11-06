from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 23_sound_and_office_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.tray = self.add_actor("tray", "tray")
        # Add objects
        self.microphone = self.add_actor("microphone", "microphone")
        self.stapler = self.add_actor("stapler", "stapler")

    def play_once(self):
        # Step 1: Pick microphone and place it into fluted_block (sound-related item)
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("pick place microphone:", success)
        if not success:
            return self.info

        # Step 2: Pick stapler and place it into tray (office tool)
        success = self.pick_and_place(self.stapler, self.tray)
        print("pick place stapler:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if microphone is on fluted_block and stapler is on tray
        if self.check_on(self.microphone, self.fluted_block) and self.check_on(self.stapler, self.tray):
            return True
        return False
