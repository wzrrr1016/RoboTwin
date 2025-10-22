
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs.utils import *
import sapien

class exclusion_task(Pick_Place_Task):
    def load_actors(self):
        # Add the wooden box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Add the non-food items
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.toycar = self.add_actor("toycar", "toycar")
        # Add the food item (apple) for reference
        self.apple = self.add_actor("apple", "apple")
    def play_once(self):
        # Place the bottle into the wooden box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("pick place bottle:", success)
        if not success:
            return self.info
        # Place the can into the wooden box
        success = self.pick_and_place(self.can, self.wooden_box)
        print("pick place can:", success)
        if not success:
            return self.info
        # Place the toycar into the wooden box
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("pick place toycar:", success)
        if not success:
            return self.info
    def check_success(self):
        # Check if all non-food items are on the wooden box
        if (self.check_on(self.bottle, self.wooden_box) and
            self.check_on(self.can, self.wooden_box) and
            self.check_on(self.toycar, self.wooden_box)):
            return True
        return False
    