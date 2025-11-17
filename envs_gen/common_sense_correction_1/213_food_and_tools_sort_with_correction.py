from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 213_food_and_tools_sort_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        - Containers: tray and wooden_box
        - Objects: knife, hammer, hamburg, french_fries, can
        - Distractors: calculator, pet-collar, toycar, book, tissue-box
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.knife = self.add_actor("knife", "knife")
        self.hammer = self.add_actor("hammer", "hammer")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.can = self.add_actor("can", "can")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "toycar", "book", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Place knife and hammer into the wooden_box
        - Place hamburg and french_fries onto the tray
        - Place can into wooden_box (wrong action), then recover by placing it onto the tray
        """
        # Step 1: Place knife into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Knife to wooden_box:", success)
        if not success:
            return self.info

        # Step 2: Place can into wooden_box (wrong action)
        success = self.pick_and_place(self.can, self.wooden_box)
        print("Can to wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover can by placing it onto the tray
        success = self.pick_and_place(self.can, self.tray)
        print("Can to tray (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place hammer into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Hammer to wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place hamburg onto the tray
        success = self.pick_and_place(self.hamburg, self.tray)
        print("Hamburg to tray:", success)
        if not success:
            return self.info

        # Step 6: Place french_fries onto the tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("French fries to tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying the final positions of all relevant objects.
        - Food and drink items (hamburg, french_fries, can) must be on the tray
        - Sharp or heavy tools (knife, hammer) must be in the wooden_box
        """
        if (
            self.check_on(self.hamburg, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.can, self.tray) and
            self.check_on(self.knife, self.wooden_box) and
            self.check_on(self.hammer, self.wooden_box)
        ):
            return True
        return False
