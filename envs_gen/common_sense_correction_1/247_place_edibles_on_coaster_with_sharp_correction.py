from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 247_place_edibles_on_coaster_with_sharp_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        Containers: coaster and dustbin.
        Objects: apple, french_fries, knife, book.
        Distractors: toycar, alarm-clock, pot-with-plant, small-speaker, shoe.
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.knife = self.add_actor("knife", "knife")
        self.book = self.add_actor("book", "book")

        # Add distractors
        distractor_list = ["toycar", "alarm-clock", "pot-with-plant", "small-speaker", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Steps:
        1. Place french_fries on the coaster.
        2. Place apple on the coaster.
        3. Place knife on the coaster (wrong action).
        4. Recover knife by placing it into the dustbin.
        5. Place book into the dustbin.
        """
        # Step 1: Place french_fries on the coaster
        success = self.pick_and_place(self.french_fries, self.coaster)
        print("Place french_fries on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place apple on the coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster:", success)
        if not success:
            return self.info

        # Step 3: Wrongly place knife on the coaster
        success = self.pick_and_place(self.knife, self.coaster)
        print("Wrongly place knife on coaster:", success)
        if not success:
            return self.info

        # Step 4: Recover knife by placing it into the dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Move knife to dustbin:", success)
        if not success:
            return self.info

        # Step 5: Place book into the dustbin
        success = self.pick_and_place(self.book, self.dustbin)
        print("Place book into dustbin:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if the task was completed successfully.
        Criteria:
        - Edible fruits and snacks (apple, french_fries) are on the coaster.
        - Sharp or non-edible items (knife, book) are in the dustbin.
        """
        if (self.check_on(self.apple, self.coaster) and
            self.check_on(self.french_fries, self.coaster) and
            self.check_on(self.knife, self.dustbin) and
            self.check_on(self.book, self.dustbin)):
            return True
        return False
