from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 486_organize_playthings_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        # Add the objects
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.toycar = self.add_actor("toycar", "toycar")
        self.drill = self.add_actor("drill", "drill")
        # Add distractors
        distractor_list = ["pot-with-plant", "book", "shoe", "alarm-clock", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place yellow block into fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        # Place blue block into fluted_block
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # Wrongly place drill into fluted_block
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Place drill (wrong):", success)
        if not success:
            return self.info

        # Recover: place drill on table
        success = self.pick_and_place(self.drill, self.table)
        print("Place drill on table:", success)
        if not success:
            return self.info

        # Place toycar into fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        # Check that yellow_block, blue_block, and toycar are in the organizer
        # And that drill is not in the organizer
        if (
            self.check_on(self.yellow_block, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            not self.check_on(self.drill, self.fluted_block)
        ):
            return True
        return False
