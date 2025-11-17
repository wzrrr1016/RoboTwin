from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 273_eating_and_drinking_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the container (fluted_block), the target objects (bread, fork, bottle),
        and other objects (stapler, toycar) as well as distractors.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects used for eating or drinking
        self.bread = self.add_actor("bread", "bread")
        self.fork = self.add_actor("fork", "fork")
        self.bottle = self.add_actor("bottle", "bottle")

        # Add other objects in the scene
        self.stapler = self.add_actor("stapler", "stapler")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractors
        distractor_list = ["pot-with-plant", "alarm-clock", "dumbbell", "shoe", "microphone"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot will:
        1. Pick and place bread, fork, and bottle into the fluted_block.
        2. Attempt to place the toycar into the fluted_block (wrong action).
        3. Correct the mistake by placing the toycar on the stapler.
        """
        # Correct actions
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Pick and place bread:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Pick and place fork:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Pick and place bottle:", success)
        if not success:
            return self.info

        # Wrong action
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Pick and place toycar (wrong):", success)
        if not success:
            return self.info

        # Recovery action
        success = self.pick_and_place(self.toycar, self.stapler)
        print("Pick and place toycar on stapler (recovery):", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was successfully completed.
        The task is considered successful if:
        - Bread, fork, and bottle are in the fluted_block.
        - The toycar is not in the fluted_block.
        """
        if (
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block) and
            not self.check_on(self.toycar, self.fluted_block)
        ):
            return True
        return False
