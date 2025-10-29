
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class exclusion_task_e2(Imagine_Task):
    def load_actors(self):
        # Container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Non-food items
        self.cup1 = self.add_actor("cup_without_handle", "cup_without_handle_0")
        self.cup2 = self.add_actor("cup_without_handle", "cup_without_handle_1")
        self.toycar = self.add_actor("toycar", "toycar")
        # Food items
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")

    def play_once(self):
        # Reasoning step: test exclusion by moving a food item and returning it
        success = self.pick_and_place(self.bread, self.table)
        print("pick place bread:", success)
        if not success:
            return self.info

        # Place non-food items into the wooden_box
        success = self.pick_and_place(self.cup1, self.wooden_box)
        print("pick place cup1:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup2, self.wooden_box)
        print("pick place cup2:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("pick place toycar:", success)
        if not success:
            return self.info

    def check_success(self):
        if (
            self.check_on(self.cup1, self.wooden_box)
            and self.check_on(self.cup2, self.wooden_box)
            and self.check_on(self.toycar, self.wooden_box)
        ):
            return True
        return False
