from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class tool_organization_correction(Imagine_Task):
    def load_actors(self):
        # Load the fluted_block and dustbin
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Load the repair tools and non-repair items
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.drill = self.add_actor("drill", "drill")
        self.mouse = self.add_actor("mouse", "mouse")

    def play_once(self):
        # Pick up the screwdriver and place it in the fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Pick and place screwdriver:", success)

        # Attempt to pick up the drill and place it in the fluted_block
        if not success:
            success = self.pick_and_place(self.drill, self.fluted_block)
            print("Pick and place drill (wrong):", success)

        # If the drill was not placed correctly, pick it up from the fluted_block and place it in the dustbin
        if not success:
            success = self.pick_and_place(self.drill, self.fluted_block)
            print("Pick and place drill (recovery):", success)
            if not success:
                success = self.pick_and_place(self.drill, self.dustbin)
                print("Pick and place drill in dustbin:", success)

        # Pick up the mouse and place it in the dustbin
        success = self.pick_and_place(self.mouse, self.dustbin)
        print("Pick and place mouse:", success)

        return success

    def check_success(self):
        # Check if the screwdriver is on the fluted_block
        if not self.check_on(self.screwdriver, self.fluted_block):
            return False

        # Check if the drill is not on the fluted_block (it should be in the dustbin)
        if self.check_on(self.drill, self.fluted_block):
            return False

        # Check if the mouse is on the dustbin
        if not self.check_on(self.mouse, self.dustbin):
            return False

        return True

# Example usage:
# task = OrganizeToolsTask()
# task.load_actors()
# success = task.play_once()
# if success:
#     print("Task completed successfully.")
# else:
#     print("Task failed.")
