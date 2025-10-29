
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class meal_assembly_recover(Imagine_Task):
    def load_actors(self):
        # Containers
        self.tray = self.add_actor("tray", "tray")
        self.shoebox = self.add_actor("shoe-box", "shoe-box")

        # Food
        self.fries = self.add_actor("french-fries", "french-fries")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.fruit = self.add_actor("fruit", "fruit")

        # Non-food (distractor)
        self.calculator = self.add_actor("calculator", "calculator")

    def play_once(self):
        # Mistake: put calculator on tray, then recover to shoe-box
        success = self.pick_and_place(self.calculator, self.tray)
        print("mistake calculator->tray:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.calculator, self.shoebox)
        print("recover calculator->shoe-box:", success)
        if not success:
            return self.info

        # Mistake: put fruit to shoe-box, then recover to tray
        success = self.pick_and_place(self.fruit, self.shoebox)
        print("mistake fruit->shoe-box:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.fruit, self.tray)
        print("recover fruit->tray:", success)
        if not success:
            return self.info

        # Correct placements: assemble meal on tray
        success = self.pick_and_place(self.fries, self.tray)
        print("place fries->tray:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.hamburg, self.tray)
        print("place hamburg->tray:", success)
        if not success:
            return self.info

    def check_success(self):
        return (
            self.check_on(self.fries, self.tray)
            and self.check_on(self.hamburg, self.tray)
            and self.check_on(self.fruit, self.tray)
            and self.check_on(self.calculator, self.shoebox)
        )
