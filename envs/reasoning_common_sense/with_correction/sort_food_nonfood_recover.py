
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class sort_food_nonfood_recover(Imagine_Task):
    def load_actors(self):
        # Containers
        self.tray = self.add_actor("tray", "tray")
        self.shoebox = self.add_actor("shoe-box", "shoe-box")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Food objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")

        # Non-food objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")

    def play_once(self):
        # Mistake: put apple into dustbin by mistake, then recover to tray
        success = self.pick_and_place(self.apple, self.dustbin)
        print("mistake place apple->dustbin:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.apple, self.tray)
        print("recover apple->tray:", success)
        if not success:
            return self.info

        # Correct placements
        success = self.pick_and_place(self.hamburg, self.tray)
        print("place hamburg->tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.shoebox)
        print("place bottle->shoe-box:", success)
        if not success:
            return self.info

        # Mistake: place can to tray, then recover to shoe-box
        success = self.pick_and_place(self.can, self.tray)
        print("mistake place can->tray:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.can, self.shoebox)
        print("recover can->shoe-box:", success)
        if not success:
            return self.info

    def check_success(self):
        # All food on tray; all non-food in shoe-box
        if (
            self.check_on(self.apple, self.tray)
            and self.check_on(self.hamburg, self.tray)
            and self.check_on(self.bottle, self.shoebox)
            and self.check_on(self.can, self.shoebox)
        ):
            return True
        return False
