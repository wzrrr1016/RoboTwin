from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class tool_organization_correction(Imagine_Task):
    def load_actors(self):
        # Load the tray and dustbin as containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Load the tools and non-repair items
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.drill = self.add_actor("drill", "drill")
        self.mug = self.add_actor("mug", "mug")
        self.book = self.add_actor("book", "book")

    def play_once(self):
        # Pick up the screwdriver and place it in the tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Pick and place screwdriver:", success)

        # Pick up the drill and place it in the tray (wrong action)
        success = self.pick_and_place(self.drill, self.tray)
        print("Pick and place drill (wrong):", success)

        # Pick up the drill from the tray and place it in the dustbin (recovery)
        success = self.pick_and_place(self.drill, self.dustbin)
        print("Pick and place drill (recovery):", success)

        # Pick up the mug and place it in the dustbin
        success = self.pick_and_place(self.mug, self.dustbin)
        print("Pick and place mug:", success)

        # Pick up the book and place it in the dustbin
        success = self.pick_and_place(self.book, self.dustbin)
        print("Pick and place book:", success)

    def check_success(self):
        # Check if all tools are in the tray and all non-repair items are in the dustbin
        success = (self.check_on(self.screwdriver, self.tray) and
                   self.check_on(self.drill, self.dustbin) and
                   self.check_on(self.mug, self.dustbin) and
                   self.check_on(self.book, self.dustbin))
        return success

# Example usage:
# task = OrganizeToolsTask()
# task.load_actors()
# task.play_once()
# if task.check_success():
#     print("Task completed successfully.")
# else:
#     print("Task failed.")
