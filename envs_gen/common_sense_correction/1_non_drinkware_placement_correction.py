from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 1_non_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the wooden_box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        # Load the non-drinkware items
        self.bread = self.add_actor("bread", "bread")
        self.hammer = self.add_actor("hammer", "hammer")
        self.scanner = self.add_actor("scanner", "scanner")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        # Load the drinkware item (mug)
        self.mug = self.add_actor("mug", "mug")

    def play_once(self):
        # Pick and place bread into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("pick place bread:", success)
        if not success:
            return self.info

        # Pick and place hammer into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("pick place hammer:", success)
        if not success:
            return self.info

        # Pick and place scanner into wooden_box
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("pick place scanner:", success)
        if not success:
            return self.info

        # Pick and place mug into wooden_box (wrong action)
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("pick place mug:", success)
        if not success:
            return self.info

        # Recovery: pick mug from wooden_box and place on table
        success = self.pick_and_place(self.mug, self.table)
        print("pick place mug on table:", success)
        if not success:
            return self.info

        # Pick and place tissue-box into wooden_box
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("pick place tissue-box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check that non-drinkware items are on wooden_box
        # and that mug is not on wooden_box
        if (self.check_on(self.bread, self.wooden_box) and
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.scanner, self.wooden_box) and
            self.check_on(self.tissue_box, self.wooden_box) and
            not self.check_on(self.mug, self.wooden_box)):
            return True
        return False
