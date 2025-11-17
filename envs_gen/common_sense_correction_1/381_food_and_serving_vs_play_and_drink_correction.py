from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 381_food_and_serving_vs_play_and_drink_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds the plate and tray as containers, and the apple, fork, toycar, and cup_without_handle as objects.
        Adds distractors as specified in the task description.
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.fork = self.add_actor("fork", "fork")
        self.toycar = self.add_actor("toycar", "toycar")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        
        # Add distractors
        distractor_list = ["screwdriver", "hammer", "book", "shoe", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The sequence includes:
        1. Wrongly placing the toycar on the plate
        2. Correcting the mistake by moving the toycar to the tray
        3. Placing edible items (apple) and utensils (fork) on the plate
        4. Placing toys (toycar) and beverage containers (cup_without_handle) on the tray
        """
        # Wrong action: Place toycar on plate (incorrect placement)
        success = self.pick_and_place(self.toycar, self.plate)
        print("Wrong placement of toycar:", success)
        if not success:
            return self.info

        # Recovery action: Move toycar from plate to tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Recovery placement of toycar:", success)
        if not success:
            return self.info

        # Place edible item (apple) on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple:", success)
        if not success:
            return self.info

        # Place utensil (fork) on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Place fork:", success)
        if not success:
            return self.info

        # Place beverage container (cup_without_handle) on tray
        success = self.pick_and_place(self.cup_without_handle, self.tray)
        print("Place cup_without_handle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all objects.
        Returns True if all objects are in their correct containers, False otherwise.
        """
        if (
            self.check_on(self.apple, self.plate) and
            self.check_on(self.fork, self.plate) and
            self.check_on(self.toycar, self.tray) and
            self.check_on(self.cup_without_handle, self.tray)
        ):
            return True
        return False
