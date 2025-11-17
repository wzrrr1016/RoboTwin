from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 219_organize_perishables_and_tools_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the organizer surface (fluted_block) as a container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the main objects involved in the task
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.hammer = self.add_actor("hammer", "hammer")
        self.book = self.add_actor("book", "book")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")

        # Add distractor objects to the environment
        distractor_list = ['toycar', 'alarm-clock', 'tissue-box', 'shoe', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm to complete the task.
        """
        # Step 1: Place apple on the organizer surface
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info

        # Step 2: Place book on the organizer surface (wrong action)
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Place book (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing book on the cup_without_handle
        success = self.pick_and_place(self.book, self.cup_without_handle)
        print("Recover book:", success)
        if not success:
            return self.info

        # Step 4: Place hammer on the organizer surface
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Place hammer:", success)
        if not success:
            return self.info

        # Step 5: Place french_fries on the organizer surface
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully based on the defined conditions.
        """
        # Check that perishable edibles and small tools are on the organizer
        correct_on = (
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.french_fries, self.fluted_block) and
            self.check_on(self.hammer, self.fluted_block)
        )

        # Check that the book is on the cup_without_handle and not on the organizer
        book_correct = (
            self.check_on(self.book, self.cup_without_handle) and
            not self.check_on(self.book, self.fluted_block)
        )

        # Check that drinkware (cup_without_handle) is not on the organizer
        drinkware_off = not self.check_on(self.cup_without_handle, self.fluted_block)

        # Return True only if all conditions are met
        return correct_on and book_correct and drinkware_off
