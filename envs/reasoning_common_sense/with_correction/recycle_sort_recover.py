
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class recycle_sort_recover(Imagine_Task):
    def load_actors(self):
        # Containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Objects
        self.can = self.add_actor("can", "can")
        self.bottle = self.add_actor("bottle", "bottle")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

    def play_once(self):
        # Mistake: put pot-with-plant into dustbin, then recover to wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.dustbin)
        print("mistake plant->dustbin:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("recover plant->wooden_box:", success)
        if not success:
            return self.info

        # Correct: recyclable items into dustbin (as proxy)
        success = self.pick_and_place(self.can, self.dustbin)
        print("place can->dustbin:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("place bottle->dustbin:", success)
        if not success:
            return self.info

    def check_success(self):
        return (
            self.check_on(self.pot_with_plant, self.wooden_box)
            and self.check_on(self.can, self.dustbin)
            and self.check_on(self.bottle, self.dustbin)
        )
