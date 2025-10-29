
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class exclusion_task_e3(Imagine_Task):
    def load_actors(self):
        # Container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Non-food items
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.toycar = self.add_actor("toycar", "toycar")
        # Food items
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")

    def play_once(self):
        # Reasoning step: intentionally pick a food item and return it
        success = self.pick_and_place(self.apple, self.table)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Place all non-food items into the wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("pick place bottle:", success)
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
        if (
            self.check_on(self.bottle, self.wooden_box)
            and self.check_on(self.can, self.wooden_box)
            and self.check_on(self.toycar, self.wooden_box)
        ):
            return True
        return False
