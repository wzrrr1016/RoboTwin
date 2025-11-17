from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 436_organize_for_use_and_storage_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds the tray and wooden_box as containers, and the relevant objects.
        Also adds the specified distractors.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects for the task
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.mouse = self.add_actor("mouse", "mouse")
        self.book = self.add_actor("book", "book")
        self.can = self.add_actor("can", "can")
        self.french_fries = self.add_actor("french_fries", "french_fries")

        # Add distractors
        distractor_list = ['sand-clock', 'tissue-box', 'dumbbell', 'purple_block', 'bell']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        - Place screwdriver and mouse on the tray.
        - Place can on the tray (wrong action).
        - Move can from tray to wooden_box (recovery).
        - Place book on the tray.
        - Place french_fries in the wooden_box.
        """
        # Place screwdriver on tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        # Place mouse on tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("Place mouse:", success)
        if not success:
            return self.info

        # Wrongly place can on tray
        success = self.pick_and_place(self.can, self.tray)
        print("Wrongly place can on tray:", success)
        if not success:
            return self.info

        # Recovery: move can from tray to wooden_box
        success = self.pick_and_place(self.can, self.wooden_box)
        print("Move can to wooden_box:", success)
        if not success:
            return self.info

        # Place book on tray
        success = self.pick_and_place(self.book, self.tray)
        print("Place book:", success)
        if not success:
            return self.info

        # Place french_fries in wooden_box
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("Place french fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - screwdriver, mouse, and book are on the tray.
        - can and french_fries are in the wooden_box.
        """
        if (self.check_on(self.screwdriver, self.tray) and
            self.check_on(self.mouse, self.tray) and
            self.check_on(self.book, self.tray) and
            self.check_on(self.can, self.wooden_box) and
            self.check_on(self.french_fries, self.wooden_box)):
            return True
        return False
