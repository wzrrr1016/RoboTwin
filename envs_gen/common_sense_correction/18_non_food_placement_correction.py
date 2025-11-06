from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 18_non_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        # Add the objects
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.bread = self.add_actor("bread", "bread")
        self.mouse = self.add_actor("mouse", "mouse")
        self.microphone = self.add_actor("microphone", "microphone")
        self.mug = self.add_actor("mug", "mug")
        self.fork = self.add_actor("fork", "fork")

    def play_once(self):
        # Recovery step: pick bread from shoe_box and place on table if it's there
        if self.check_on(self.bread, self.shoe_box):
            success = self.pick_and_place(self.bread, self.table)
            print("pick place bread:", success)
            if not success:
                return self.info

        # Pick and place non-food items into shoe_box
        success = self.pick_and_place(self.orange_block, self.shoe_box)
        print("pick place orange_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("pick place mouse:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.microphone, self.shoe_box)
        print("pick place microphone:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mug, self.shoe_box)
        print("pick place mug:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.fork, self.shoe_box)
        print("pick place fork:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all non-food items are on the shoe_box
        if (self.check_on(self.orange_block, self.shoe_box) and
            self.check_on(self.mouse, self.shoe_box) and
            self.check_on(self.microphone, self.shoe_box) and
            self.check_on(self.mug, self.shoe_box) and
            self.check_on(self.fork, self.shoe_box)):
            return True
        return False
