from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 230_tool_and_office_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (containers and objects) into the simulation environment.
        Adds the fluted_block and shoe_box as containers, and the screwdriver, hammer, mouse, and markpen as objects.
        Adds distractors as specified in the task description.
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.hammer = self.add_actor("hammer", "hammer")
        self.mouse = self.add_actor("mouse", "mouse")
        self.markpen = self.add_actor("markpen", "markpen")

        # Add distractors
        distractors = ["apple", "baguette", "jam-jar", "pot-with-plant", "milk-box"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot first places the screwdriver into the wrong container (shoe_box), then recovers it to the correct one (fluted_block).
        It then places the hammer into fluted_block and the mouse and markpen into shoe_box.
        """
        # Step 1: Place screwdriver into shoe_box (wrong action)
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Place screwdriver into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recover screwdriver to fluted_block (correct action)
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Recover screwdriver to fluted_block:", success)
        if not success:
            return self.info

        # Step 3: Place hammer into fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Place hammer into fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Place mouse into shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Place mouse into shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place markpen into shoe_box
        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Place markpen into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The task is considered successful if:
        - The screwdriver and hammer are in the fluted_block.
        - The mouse and markpen are in the shoe_box.
        """
        if (
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.mouse, self.shoe_box) and
            self.check_on(self.markpen, self.shoe_box)
        ):
            return True
        return False
