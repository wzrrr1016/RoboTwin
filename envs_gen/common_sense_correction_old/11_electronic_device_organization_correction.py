from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 11_electronic_device_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.tray = self.add_actor("tray", "tray")
        # Add objects
        self.knife = self.add_actor("knife", "knife")
        self.microphone = self.add_actor("microphone", "microphone")
        self.scanner = self.add_actor("scanner", "scanner")

    def play_once(self):
        # Step 1: Pick knife and place into tray (correct action)
        success = self.pick_and_place(self.knife, self.tray)
        print("pick place knife:", success)
        if not success:
            return self.info

        # Step 2: Pick microphone and place into fluted_block
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("pick place microphone:", success)
        if not success:
            return self.info

        # Step 3: Pick scanner and place into fluted_block
        success = self.pick_and_place(self.scanner, self.fluted_block)
        print("pick place scanner:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if knife is on tray (non-electronic)
        knife_on_tray = self.check_on(self.knife, self.tray)
        # Check if microphone and scanner are on fluted_block (electronic)
        mic_on_fluted = self.check_on(self.microphone, self.fluted_block)
        scanner_on_fluted = self.check_on(self.scanner, self.fluted_block)
        return knife_on_tray and mic_on_fluted and scanner_on_fluted
