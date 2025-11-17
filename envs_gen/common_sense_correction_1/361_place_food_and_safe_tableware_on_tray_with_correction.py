from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 361_place_food_and_safe_tableware_on_tray_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        Adds the tray, edible foods, tableware, and book as actors.
        Adds distractor objects to the environment.
        """
        # Add the tray as a container
        self.tray = self.add_actor("tray", "tray")
        
        # Add edible foods
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add safe tableware
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        
        # Add book (non-edible, non-tableware)
        self.book = self.add_actor("book", "book")
        
        # Add distractor objects to the environment
        distractor_list = ["screwdriver", "hammer", "toycar", "shoe", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Place bread on tray
        2. Place fork on tray
        3. Place book on tray (wrong action)
        4. Recover book by placing it on table
        5. Place french fries on tray
        6. Place knife on table
        """
        # Step 1: Place bread on tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread:", success)
        if not success:
            return self.info

        # Step 2: Place fork on tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick fork:", success)
        if not success:
            return self.info

        # Step 3: Place book on tray (wrong action)
        success = self.pick_and_place(self.book, self.tray)
        print("Pick book (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover book by placing it on table
        success = self.pick_and_place(self.book, self.table)
        print("Recover book:", success)
        if not success:
            return self.info

        # Step 5: Place french fries on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Pick french fries:", success)
        if not success:
            return self.info

        # Step 6: Place knife on table
        success = self.pick_and_place(self.knife, self.table)
        print("Pick knife:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Bread and french fries (edible foods) are on the tray
        - Fork (safe tableware) is on the tray
        - Book is not on the tray (it was recovered to the table)
        - Knife is on the table (not on the tray)
        """
        return (
            self.check_on(self.bread, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.fork, self.tray) and
            not self.check_on(self.book, self.tray) and
            self.check_on(self.knife, self.table)
        )
