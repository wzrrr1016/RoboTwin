from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 343_reusable_and_disposable_grouping_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the simulation environment"""
        # Add the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add task-specific objects
        self.mug = self.add_actor("mug", "mug")
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.book = self.add_actor("book", "book")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects
        distractor_list = ["apple", "baguette", "french_fries", "hamburg"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions for the task"""
        # Place book on organizer
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Place book on fluted_block:", success)
        if not success:
            return self.info

        # Place mug on organizer
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug on fluted_block:", success)
        if not success:
            return self.info

        # Place tissue-box on organizer (wrong placement)
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box on fluted_block (wrong):", success)
        if not success:
            return self.info

        # Correct placement - move tissue-box to book
        success = self.pick_and_place(self.tissue_box, self.book)
        print("Place tissue-box on book (recovery):", success)
        if not success:
            return self.info

        # Place bottle on organizer
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle on fluted_block:", success)
        if not success:
            return self.info

        # Place can on organizer
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Place can on fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        return (
            self.check_on(self.book, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.can, self.fluted_block) and
            self.check_on(self.tissue_box, self.book)
        )
