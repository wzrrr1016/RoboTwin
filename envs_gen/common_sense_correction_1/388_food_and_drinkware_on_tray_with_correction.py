from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 388_food_and_drinkware_on_tray_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Distractors are also added to simulate a realistic scene.
        """
        # Add the tray as the main container
        self.tray = self.add_actor("tray", "tray")

        # Add ready-to-eat foods and drinkware
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")

        # Add toycar for the wrong action and recovery
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractors to the environment
        distractor_list = ['battery', 'stapler', 'pot-with-plant', 'microphone', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        This includes a wrong action and a recovery step, followed by placing the correct items.
        """
        # Wrong action: Place toycar on tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Place toycar on tray (wrong):", success)
        if not success:
            return self.info

        # Recovery: Place toycar back on the table
        success = self.pick_and_place(self.toycar, self.table)
        print("Recover toycar to table:", success)
        if not success:
            return self.info

        # Place ready-to-eat foods and drinkware on the tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Place apple on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french fries on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.tray)
        print("Place bottle on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Place cup with handle on tray:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying that all required
        ready-to-eat foods and drinkware are placed on the tray.
        """
        # Check if all required items are on the tray
        if (
            self.check_on(self.apple, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.bottle, self.tray) and
            self.check_on(self.cup_with_handle, self.tray)
        ):
            return True
        return False
