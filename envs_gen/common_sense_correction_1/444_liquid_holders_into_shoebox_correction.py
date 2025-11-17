from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 444_liquid_holders_into_shoebox_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the container (shoe_box), the target objects (shampoo, bottle, cup_with_handle, book),
        and the distractor objects.
        """
        # Add the container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add the target objects
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.book = self.add_actor("book", "book")

        # Add distractor objects
        distractor_list = ["calculator", "hammer", "toycar", "battery", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot will:
        1. Pick shampoo and place it in the shoe_box.
        2. Pick bottle and place it in the shoe_box.
        3. Pick book and place it in the shoe_box (this is a wrong action).
        4. Pick book from the shoe_box and place it on the table (recovery).
        5. Pick cup_with_handle and place it in the shoe_box.
        """
        # Step 1: Pick shampoo and place into shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Pick shampoo:", success)
        if not success:
            return self.info

        # Step 2: Pick bottle and place into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Pick bottle:", success)
        if not success:
            return self.info

        # Step 3: Pick book and place into shoe_box (wrong action)
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Pick book (wrong):", success)
        if not success:
            return self.info

        # Step 4: Pick book from shoe_box and place on table (recovery)
        success = self.pick_and_place(self.book, self.table)
        print("Recover book:", success)
        if not success:
            return self.info

        # Step 5: Pick cup_with_handle and place into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Pick cup_with_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was successfully completed.
        The task is considered successful if:
        - shampoo is on the shoe_box
        - bottle is on the shoe_box
        - cup_with_handle is on the shoe_box
        - book is NOT on the shoe_box
        """
        if (
            self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.bottle, self.shoe_box) and
            self.check_on(self.cup_with_handle, self.shoe_box) and
            not self.check_on(self.book, self.shoe_box)
        ):
            return True
        return False
