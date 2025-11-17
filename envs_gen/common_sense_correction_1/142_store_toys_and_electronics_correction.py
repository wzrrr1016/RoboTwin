from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 142_store_toys_and_electronics_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds the tray and wooden_box as containers, and the relevant objects.
        Adds distractors as specified in the task description.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.green_block = self.add_actor("green_block", "green_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.microphone = self.add_actor("microphone", "microphone")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractors
        distractor_list = ["book", "can", "shoe", "baguette"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        Includes placing objects on the tray, a wrong placement of the dumbbell,
        and a recovery step to move the dumbbell to the wooden_box.
        """
        # Place green_block on tray
        success = self.pick_and_place(self.green_block, self.tray)
        print("Place green_block:", success)
        if not success:
            return self.info

        # Place microphone on tray
        success = self.pick_and_place(self.microphone, self.tray)
        print("Place microphone:", success)
        if not success:
            return self.info

        # Wrong placement of dumbbell on tray
        success = self.pick_and_place(self.dumbbell, self.tray)
        print("Wrong placement of dumbbell:", success)
        if not success:
            return self.info

        # Recovery: move dumbbell to wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Recover dumbbell:", success)
        if not success:
            return self.info

        # Place purple_block on tray
        success = self.pick_and_place(self.purple_block, self.tray)
        print("Place purple_block:", success)
        if not success:
            return self.info

        # Place orange_block on tray
        success = self.pick_and_place(self.orange_block, self.tray)
        print("Place orange_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        Verifies that all lightweight colorful toys and delicate electronics are on the tray,
        and the heavy exercise gear is in the wooden_box.
        """
        if (
            self.check_on(self.green_block, self.tray) and
            self.check_on(self.purple_block, self.tray) and
            self.check_on(self.orange_block, self.tray) and
            self.check_on(self.microphone, self.tray) and
            self.check_on(self.dumbbell, self.wooden_box)
        ):
            return True
        return False
