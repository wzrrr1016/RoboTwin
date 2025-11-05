from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class tool_storage_correction_50(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.book = self.add_actor("book", "book")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.mug = self.add_actor("mug", "mug")

    def play_once(self):
        # Pick hammer and place into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("pick place hammer:", success)
        if not success:
            return self.info

        # Pick screwdriver and place into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("pick place screwdriver:", success)
        if not success:
            return self.info

        # Pick book and place into plate
        success = self.pick_and_place(self.book, self.plate)
        print("pick place book:", success)
        if not success:
            return self.info

        # Pick shampoo and place into plate
        success = self.pick_and_place(self.shampoo, self.plate)
        print("pick place shampoo:", success)
        if not success:
            return self.info

        # Pick mug and place into plate
        success = self.pick_and_place(self.mug, self.plate)
        print("pick place mug:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if metal tools are in wooden_box
        if not (self.check_on(self.hammer, self.wooden_box) and self.check_on(self.screwdriver, self.wooden_box)):
            return False

        # Check if non-metal items are in plate
        if not (self.check_on(self.book, self.plate) and self.check_on(self.shampoo, self.plate) and self.check_on(self.mug, self.plate)):
            return False

        return True
