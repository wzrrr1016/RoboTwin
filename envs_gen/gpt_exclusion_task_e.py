
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs.utils import *
import sapien

class gpt_exclusion_task_e(Pick_Place_Task):
    def load_actors(self):
        # Load the two cups
        self.cup1 = self.add_actor("cup_without_handle", "cup_without_handle_0")
        self.cup2 = self.add_actor("cup_without_handle", "cup_without_handle_1")
        # Load the bread (food)
        self.bread = self.add_actor("bread", "bread")
        # Load the toycar (non-food)
        self.toycar = self.add_actor("toycar", "toycar")
        # Load the apple (food)
        self.apple = self.add_actor("apple", "apple")
        # Load the can (non-food)
        self.can = self.add_actor("can", "can")
        # Load the wooden-box (container)
        self.wooden_box = self.add_actor("wooden-box", "wooden-box")
    def play_once(self):
        # Step 1: Accidentally grasp the apple and put it back on the table
        success = self.pick_and_place(self.apple, self.table)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Step 2: Place the two cups, can, and toycar into the wooden-box
        # Place cup1
        success = self.pick_and_place(self.cup1, self.wooden_box)
        print("pick place cup1:", success)
        if not success:
            return self.info

        # Place cup2
        success = self.pick_and_place(self.cup2, self.wooden_box)
        print("pick place cup2:", success)
        if not success:
            return self.info

        # Place can
        success = self.pick_and_place(self.can, self.wooden_box)
        print("pick place can:", success)
        if not success:
            return self.info

        # Place toycar
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("pick place toycar:", success)
        if not success:
            return self.info
    def check_success(self):
        # Check if all non-food items are on the wooden-box
        if (self.check_on(self.cup1, self.wooden_box) and
            self.check_on(self.cup2, self.wooden_box) and
            self.check_on(self.can, self.wooden_box) and
            self.check_on(self.toycar, self.wooden_box)):
            return True
        return False
    