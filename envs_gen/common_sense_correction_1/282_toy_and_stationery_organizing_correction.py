from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 282_toy_and_stationery_organizing_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the objects to be manipulated
        self.toycar = self.add_actor("toycar", "toycar")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.markpen = self.add_actor("markpen", "markpen")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors as specified in the task
        distractor_list = ["apple", "baguette", "pot-with-plant", "alarm-clock", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrongly place the screwdriver into the fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Wrong placement of screwdriver:", success)
        if not success:
            return self.info

        # Step 2: Recovery - place the screwdriver back on the table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Recovering screwdriver:", success)
        if not success:
            return self.info

        # Step 3: Place toycar into the fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

        # Step 4: Place purple_block into the fluted_block
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Place purple_block:", success)
        if not success:
            return self.info

        # Step 5: Place markpen into the fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Place markpen:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check that the repair tool (screwdriver) is not on the fluted_block
        if self.check_on(self.screwdriver, self.fluted_block):
            return False

        # Check that the children's toys and stationery are on the fluted_block
        if (
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.purple_block, self.fluted_block) and
            self.check_on(self.markpen, self.fluted_block)
        ):
            return True

        return False
