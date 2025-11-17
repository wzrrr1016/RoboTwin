from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 184_perishable_foods_and_protection_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Adds the required objects, containers, and distractors.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add required objects
        self.apple = self.add_actor("apple", "apple")
        self.book = self.add_actor("book", "book")
        self.bread = self.add_actor("bread", "bread")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")

        # Add distractors
        distractor_list = ['shoe', 'dumbbell', 'toycar', 'red_block', 'pot-with-plant', 'hammer']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot places perishable foods on the tray and electronics/paper items in the wooden box.
        """
        # Step 1: Pick apple and place it on the tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Apple to tray:", success)
        if not success:
            return self.info

        # Step 2: Pick book and place it on the tray (wrong action)
        success = self.pick_and_place(self.book, self.tray)
        print("Book to tray (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick book from tray and place it into the wooden_box (recovery)
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Book to wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Pick bread and place it on the tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Bread to tray:", success)
        if not success:
            return self.info

        # Step 5: Pick small-speaker and place it into the wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Small-speaker to wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        Perishable foods (apple, bread) must be on the tray.
        Electronics (small-speaker) and paper items (book) must be in the wooden_box.
        """
        # Check if perishable foods are on the tray
        apple_on_tray = self.check_on(self.apple, self.tray)
        bread_on_tray = self.check_on(self.bread, self.tray)

        # Check if electronics and paper items are in the wooden_box
        book_in_wooden = self.check_on(self.book, self.wooden_box)
        speaker_in_wooden = self.check_on(self.small_speaker, self.wooden_box)

        # Return True only if all conditions are met
        return all([apple_on_tray, bread_on_tray, book_in_wooden, speaker_in_wooden])
