from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 109_organize_tools_and_recyclables_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers, objects, and distractors.
        """
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects used for the task
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.bottle = self.add_actor("bottle", "bottle")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractor objects to the environment
        distractors = ["pot-with-plant", "shoe", "book", "tissue-box", "alarm-clock"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot places repair and play items on the fluted_block and moves
        recyclable items (bottle) to the dustbin.
        """
        # Place hammer on fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Place hammer on fluted_block:", success)
        if not success:
            return self.info

        # Place screwdriver on fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver on fluted_block:", success)
        if not success:
            return self.info

        # Place bottle on fluted_block (wrong action)
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle on fluted_block (wrong):", success)
        if not success:
            return self.info

        # Correct the mistake: move bottle to dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Move bottle to dustbin:", success)
        if not success:
            return self.info

        # Place toycar on fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar on fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The success condition is:
        - Hammer, screwdriver, and toycar are on the fluted_block
        - Bottle is in the dustbin
        """
        if (
            self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.bottle, self.dustbin)
        ):
            return True
        return False
