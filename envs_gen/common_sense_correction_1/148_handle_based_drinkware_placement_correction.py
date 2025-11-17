from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 148_handle_based_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (containers and objects) into the simulation environment.
        Distractors are also added to simulate a realistic cluttered scene.
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add drinkware objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.can = self.add_actor("can", "can")
        self.bottle = self.add_actor("bottle", "bottle")

        # Add distractors to the environment
        distractor_list = ["calculator", "toycar", "alarm-clock", "book", "markpen"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The robot places drinkware with handles on the fluted_block and
        drinkware without handles into the shoe_box. A recovery step is included
        to correct a wrong placement of the bottle.
        """
        # Step 1: Place mug (with handle) on fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug on fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Place can (no handle) into shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Place can into shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Place bottle (no handle) on fluted_block (wrong placement)
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle on fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover by placing bottle into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Recover bottle to shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place cup_without_handle (no handle) into shoe_box
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("Place cup_without_handle into shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions
        of all drinkware objects in the correct containers.
        """
        if (
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.can, self.shoe_box) and
            self.check_on(self.bottle, self.shoe_box) and
            self.check_on(self.cup_without_handle, self.shoe_box)
        ):
            return True
        return False
