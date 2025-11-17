from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 55_serve_drinkware_on_tray_with_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the environment."""
        # Add the main container
        self.tray = self.add_actor("tray", "tray")
        
        # Add drinkware and non-drinkware objects
        self.mug = self.add_actor("mug", "mug_0")
        self.cup = self.add_actor("cup", "cup_0")
        self.book = self.add_actor("book", "book_0")
        self.bread = self.add_actor("bread", "bread_0")
        self.green_block = self.add_actor("green_block", "green_block_0")
        
        # Add distractor objects
        distractor_list = ["screwdriver", "toycar", "alarm-clock", "dumbbell", "microphone"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's sequence of actions for the task."""
        # Initial wrong action: place book on tray
        success = self.pick_and_place(self.book, self.tray)
        print("Pick book and place on tray (wrong):", success)
        if not success:
            return self.info

        # Recovery action: move book back to table
        success = self.pick_and_place(self.book, self.table)
        print("Pick book from tray and place on table (recovery):", success)
        if not success:
            return self.info

        # Correct actions for drinkware
        success = self.pick_and_place(self.mug, self.tray)
        print("Pick mug and place on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup, self.tray)
        print("Pick cup and place on tray:", success)
        if not success:
            return self.info

        # Correct actions for non-drinkware
        success = self.pick_and_place(self.bread, self.table)
        print("Pick bread and place on table:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.table)
        print("Pick green_block and place on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        return (
            self.check_on(self.mug, self.tray) and
            self.check_on(self.cup, self.tray) and
            self.check_on(self.book, self.table) and
            self.check_on(self.bread, self.table) and
            self.check_on(self.green_block, self.table)
        )
