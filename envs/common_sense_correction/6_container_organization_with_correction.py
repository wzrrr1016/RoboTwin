from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class container_organization_with_correction_6(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add objects
        self.mouse = self.add_actor("mouse", "mouse")
        self.stapler = self.add_actor("stapler", "stapler")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.knife = self.add_actor("knife", "knife")

    def play_once(self):
        # Pick mouse and place into tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("pick place mouse:", success)
        if not success:
            return self.info

        # Pick stapler and place into tray
        success = self.pick_and_place(self.stapler, self.tray)
        print("pick place stapler:", success)
        if not success:
            return self.info

        # Pick bottle and place into dustbin (wrong)
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("pick place bottle (wrong):", success)
        if not success:
            return self.info

        # Pick bottle from dustbin and place into tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("pick place bottle (correct):", success)
        if not success:
            return self.info

        # Pick cup_without_handle and place into dustbin
        success = self.pick_and_place(self.cup_without_handle, self.dustbin)
        print("pick place cup_without_handle:", success)
        if not success:
            return self.info

        # Pick knife and place into dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("pick place knife:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all required objects are in the correct containers
        mouse_on_tray = self.check_on(self.mouse, self.tray)
        stapler_on_tray = self.check_on(self.stapler, self.tray)
        bottle_on_tray = self.check_on(self.bottle, self.tray)
        cup_on_dustbin = self.check_on(self.cup_without_handle, self.dustbin)
        knife_on_dustbin = self.check_on(self.knife, self.dustbin)

        return mouse_on_tray and stapler_on_tray and bottle_on_tray and cup_on_dustbin and knife_on_dustbin
