from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class tool_storage_rearrangement_correction_8(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.table = self.add_actor("table", "table")
        # Add objects
        self.drill = self.add_actor("drill", "drill")
        self.hammer = self.add_actor("hammer", "hammer")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.book = self.add_actor("book", "book")

    def play_once(self):
        # Place drill (power tool) into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("pick place drill:", success)
        if not success:
            return self.info

        # Place hammer (hand tool) on table
        success = self.pick_and_place(self.hammer, self.table)
        print("pick place hammer:", success)
        if not success:
            return self.info

        # Place dumbbell (hand tool) on table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("pick place dumbbell:", success)
        if not success:
            return self.info

        # Place screwdriver (power tool) into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("pick place screwdriver:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if power tools (drill, screwdriver) are in wooden_box
        if self.check_on(self.drill, self.wooden_box) and self.check_on(self.screwdriver, self.wooden_box):
            # Check if hand tools (hammer, dumbbell) are on table
            if self.check_on(self.hammer, self.table) and self.check_on(self.dumbbell, self.table):
                return True
        return False
