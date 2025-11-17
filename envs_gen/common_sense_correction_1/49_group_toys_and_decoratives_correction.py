from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 49_group_toys_and_decoratives_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.toycar = self.add_actor("toycar", "toycar")
        self.mouse = self.add_actor("mouse", "mouse")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractors
        distractor_list = ["apple", "chips-tub", "baguette", "jam-jar", "milk-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place blue_block on tray
        success = self.pick_and_place(self.blue_block, self.tray)
        print("Place blue_block on tray:", success)
        if not success:
            return self.info

        # Place orange_block on tray
        success = self.pick_and_place(self.orange_block, self.tray)
        print("Place orange_block on tray:", success)
        if not success:
            return self.info

        # Place toycar on tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Place toycar on tray:", success)
        if not success:
            return self.info

        # Wrong placement: mouse on coaster
        success = self.pick_and_place(self.mouse, self.coaster)
        print("Wrong: Place mouse on coaster:", success)
        if not success:
            return self.info

        # Recovery: mouse to tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("Recover: Place mouse on tray:", success)
        if not success:
            return self.info

        # Place pot-with-plant on coaster
        success = self.pick_and_place(self.pot_with_plant, self.coaster)
        print("Place pot-with-plant on coaster:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check all required objects are in the correct containers
        if (
            self.check_on(self.blue_block, self.tray) and
            self.check_on(self.orange_block, self.tray) and
            self.check_on(self.toycar, self.tray) and
            self.check_on(self.mouse, self.tray) and
            self.check_on(self.pot_with_plant, self.coaster)
        ):
            return True
        return False
