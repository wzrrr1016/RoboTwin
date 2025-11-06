from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 49_non_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the wooden_box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the non-tool items
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

    def play_once(self):
        # Place cup_without_handle into wooden_box
        success = self.pick_and_place(self.cup_without_handle, self.wooden_box)
        print("pick place cup_without_handle:", success)
        if not success:
            return self.info

        # Place cup_with_handle into wooden_box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info

        # Place pot_with_plant into wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("pick place pot_with_plant:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all non-tool items are on the wooden_box
        if (self.check_on(self.cup_without_handle, self.wooden_box) and
            self.check_on(self.cup_with_handle, self.wooden_box) and
            self.check_on(self.pot_with_plant, self.wooden_box)):
            return True
        return False
