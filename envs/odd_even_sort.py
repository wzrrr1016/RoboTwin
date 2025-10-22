
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs.utils import *
import sapien

class odd_even_sort(Pick_Place_Task):
    def load_actors(self):
        # Load containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe-box", "shoe-box")

        # Load items
        self.bottle_0 = self.add_actor("bottle", "bottle_0")
        self.bottle_1 = self.add_actor("bottle", "bottle_1")
        self.bottle_2 = self.add_actor("bottle", "bottle_2")
        self.can_0 = self.add_actor("can", "can_0")
        self.can_1 = self.add_actor("can", "can_1")
        self.toycar = self.add_actor("toycar", "toycar")
    def play_once(self):
        # Place 3 bottles and 1 toycar into the shoe-box
        success = self.pick_and_place(self.bottle_0, self.shoe_box)
        print("pick place bottle_0:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle_1, self.shoe_box)
        print("pick place bottle_1:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle_2, self.shoe_box)
        print("pick place bottle_2:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("pick place toycar:", success)
        if not success:
            return self.info

        # Place 2 cans onto the tray
        success = self.pick_and_place(self.can_0, self.tray)
        print("pick place can_0:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can_1, self.tray)
        print("pick place can_1:", success)
        if not success:
            return self.info
    def check_success(self):
        # Check all 3 bottles and toycar are on the shoe-box
        if (self.check_on(self.bottle_0, self.shoe_box) and
            self.check_on(self.bottle_1, self.shoe_box) and
            self.check_on(self.bottle_2, self.shoe_box) and
            self.check_on(self.toycar, self.shoe_box)):

            # Check both cans are on the tray
            if (self.check_on(self.can_0, self.tray) and
                self.check_on(self.can_1, self.tray)):
                return True

        return False
    