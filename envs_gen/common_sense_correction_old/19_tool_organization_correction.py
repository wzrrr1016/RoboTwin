from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 19_tool_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.bell = self.add_actor("bell", "bell")
        self.mouse = self.add_actor("mouse", "mouse")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")

    def play_once(self):
        # Step 1: Pick screwdriver and place into tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("pick place screwdriver:", success)
        if not success:
            return self.info

        # Step 2: Pick purple_block and place into tray (wrong)
        success = self.pick_and_place(self.purple_block, self.tray)
        print("pick place purple_block:", success)
        if not success:
            return self.info

        # Step 3: Pick purple_block from tray and place into dustbin
        success = self.pick_and_place(self.purple_block, self.dustbin)
        print("pick place purple_block to dustbin:", success)
        if not success:
            return self.info

        # Step 4: Pick bell and place into dustbin
        success = self.pick_and_place(self.bell, self.dustbin)
        print("pick place bell:", success)
        if not success:
            return self.info

        # Step 5: Pick mouse and place into dustbin
        success = self.pick_and_place(self.mouse, self.dustbin)
        print("pick place mouse:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check screwdriver is on tray
        if not self.check_on(self.screwdriver, self.tray):
            return False

        # Check purple_block is on dustbin
        if not self.check_on(self.purple_block, self.dustbin):
            return False

        # Check bell is on dustbin
        if not self.check_on(self.bell, self.dustbin):
            return False

        # Check mouse is on dustbin
        if not self.check_on(self.mouse, self.dustbin):
            return False

        # Check cup_without_handle is on dustbin
        if not self.check_on(self.cup_without_handle, self.dustbin):
            return False

        return True
