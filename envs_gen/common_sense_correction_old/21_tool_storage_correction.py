from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 21_tool_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.coaster = self.add_actor("coaster", "coaster")
        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.bottle = self.add_actor("bottle", "bottle")
        self.book = self.add_actor("book", "book")

    def play_once(self):
        # Place hammer in shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("pick place hammer:", success)
        if not success:
            return self.info
        # Place dumbbell in shoe_box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("pick place dumbbell:", success)
        if not success:
            return self.info
        # Place shampoo in coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("pick place shampoo:", success)
        if not success:
            return self.info
        # Place bottle in coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("pick place bottle:", success)
        if not success:
            return self.info
        # Place book in coaster
        success = self.pick_and_place(self.book, self.coaster)
        print("pick place book:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if hammer and dumbbell are in shoe_box
        if self.check_on(self.hammer, self.shoe_box) and self.check_on(self.dumbbell, self.shoe_box):
            # Check if shampoo, bottle, and book are in coaster
            if self.check_on(self.shampoo, self.coaster) and self.check_on(self.bottle, self.coaster) and self.check_on(self.book, self.coaster):
                return True
        return False
