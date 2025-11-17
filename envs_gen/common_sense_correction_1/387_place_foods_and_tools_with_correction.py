from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 387_place_foods_and_tools_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Distractors are also added to the environment.
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.teanet = self.add_actor("teanet", "teanet")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "alarm-clock", "shoe", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        This includes placing objects in the correct containers and recovering from a wrong placement.
        """
        # Step 1: Place yellow_block on tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Place yellow_block on tray:", success)
        if not success:
            return self.info

        # Step 2: Place teanet on tray
        success = self.pick_and_place(self.teanet, self.tray)
        print("Place teanet on tray:", success)
        if not success:
            return self.info

        # Step 3: Wrongly place apple on tray (to be recovered)
        success = self.pick_and_place(self.apple, self.tray)
        print("Wrongly place apple on tray:", success)
        if not success:
            return self.info

        # Step 4: Recovery: Move apple from tray to plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Recover apple to plate:", success)
        if not success:
            return self.info

        # Step 5: Place french_fries on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries on plate:", success)
        if not success:
            return self.info

        # Step 6: Place purple_block on tray
        success = self.pick_and_place(self.purple_block, self.tray)
        print("Place purple_block on tray:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all objects.
        """
        if (
            self.check_on(self.apple, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.teanet, self.tray) and
            self.check_on(self.yellow_block, self.tray) and
            self.check_on(self.purple_block, self.tray)
        ):
            return True
        return False
