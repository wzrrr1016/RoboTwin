
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs.utils import *
import sapien

class gpt_symmetrical_pairing(Pick_Place_Task):
    def load_actors(self):
        # Add two bowls
        self.bowl1 = self.add_actor("bowl", "bowl_0")
        self.bowl2 = self.add_actor("bowl", "bowl_1")
        # Add the four items
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.hamburger = self.add_actor("hamburger", "hamburger")
        self.apple = self.add_actor("apple", "apple")
    def play_once(self):
        # Place bottle and can into bowl1
        success = self.pick_and_place(self.bottle, self.bowl1)
        print("pick place bottle:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.can, self.bowl1)
        print("pick place can:", success)
        if not success:
            return self.info

        # Place hamburger and apple into bowl2
        success = self.pick_and_place(self.hamburger, self.bowl2)
        print("pick place hamburger:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.apple, self.bowl2)
        print("pick place apple:", success)
        if not success:
            return self.info
    def check_success(self):
        # Count items on each bowl
        count_bowl1 = 0
        if self.check_on(self.bottle, self.bowl1):
            count_bowl1 += 1
        if self.check_on(self.can, self.bowl1):
            count_bowl1 += 1
        if self.check_on(self.hamburger, self.bowl1):
            count_bowl1 += 1
        if self.check_on(self.apple, self.bowl1):
            count_bowl1 += 1

        count_bowl2 = 0
        if self.check_on(self.bottle, self.bowl2):
            count_bowl2 += 1
        if self.check_on(self.can, self.bowl2):
            count_bowl2 += 1
        if self.check_on(self.hamburger, self.bowl2):
            count_bowl2 += 1
        if self.check_on(self.apple, self.bowl2):
            count_bowl2 += 1

        # Check if both bowls have exactly two items
        return count_bowl1 == 2 and count_bowl2 == 2
    