
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs.utils import *
import sapien

class gpt_meal_composition_capacity(Pick_Place_Task):
    def load_actors(self):
        # Add the tray and bowl as containers
        self.tray = self.add_actor("tray", "tray")
        self.bowl = self.add_actor("bowl", "bowl")

        # Add the objects on the table
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.toycar = self.add_actor("toycar", "toycar")
    def play_once(self):
        # Place the bottle on the tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("pick place bottle:", success)
        if not success:
            return self.info

        # Place the hamburger on the tray
        success = self.pick_and_place(self.hamburg, self.tray)
        print("pick place hamburger:", success)
        if not success:
            return self.info

        # Place the apple on the tray
        success = self.pick_and_place(self.apple, self.tray)
        print("pick place apple:", success)
        if not success:
            return self.info

        # Place the can in the bowl
        success = self.pick_and_place(self.can, self.bowl)
        print("pick place can:", success)
        if not success:
            return self.info

        # Place the bread in the bowl
        success = self.pick_and_place(self.bread, self.bowl)
        print("pick place bread:", success)
        if not success:
            return self.info
    def check_success(self):
        # Check that the tray has the bottle, hamburger, and apple
        if not (self.check_on(self.bottle, self.tray) and
                self.check_on(self.hamburg, self.tray) and
                self.check_on(self.apple, self.tray)):
            return False

        # Check that the bowl has the can and bread
        if not (self.check_on(self.can, self.bowl) and
                self.check_on(self.bread, self.bowl)):
            return False

        return True
    