
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class exclusion_task_e1(Imagine_Task):
    def load_actors(self):
        # Container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Non-food items
        self.bottle1 = self.add_actor("bottle", "bottle_0")
        self.bottle2 = self.add_actor("bottle", "bottle_1")
        self.can = self.add_actor("can", "can")
        self.toycar = self.add_actor("toycar", "toycar")
        # Food item (distractor)
        self.apple = self.add_actor("apple", "apple")

    def play_once(self):
        # Reasoning step: accidentally grasp the apple and put it back on the table
        success = self.pick_and_place(self.apple, self.table)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Place all non-food items into the wooden_box
        success = self.pick_and_place(self.bottle1, self.wooden_box)
        print("pick place bottle1:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle2, self.wooden_box)
        print("pick place bottle2:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can, self.wooden_box)
        print("pick place can:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("pick place toycar:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check that all non-food items are on the wooden_box
        if (
            self.check_on(self.bottle1, self.wooden_box)
            and self.check_on(self.bottle2, self.wooden_box)
            and self.check_on(self.can, self.wooden_box)
            and self.check_on(self.toycar, self.wooden_box)
        ):
            return True
        return False
