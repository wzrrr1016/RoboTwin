from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 270_tray_edibles_and_utensils_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Tray is the container.
        - Edible items: apple, bread.
        - Eating utensils: fork, knife.
        - Shampoo is a non-edible item that will be mistakenly placed and then removed.
        - Distractors are added to simulate a cluttered environment.
        """
        # Add the tray as the main container
        self.tray = self.add_actor("tray", "tray")

        # Add edible items
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")

        # Add eating utensils
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")

        # Add shampoo (non-edible, will be placed and then removed)
        self.shampoo = self.add_actor("shampoo", "shampoo")

        # Add distractors to the environment
        distractors = ["calculator", "screwdriver", "toycar", "pot-with-plant", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Pick apple and place it on the tray.
        2. Pick shampoo and place it on the tray (wrong action).
        3. Pick shampoo from the tray and place it on the table (recovery).
        4. Pick bread and place it on the tray.
        5. Pick fork and place it on the tray.
        6. Pick knife and place it on the tray.
        """
        # Step 1: Pick apple and place on tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Pick apple:", success)
        if not success:
            return self.info

        # Step 2: Pick shampoo and place on tray (wrong action)
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick shampoo (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick shampoo from tray and place on table (recovery)
        success = self.pick_and_place(self.shampoo, self.table)
        print("Recover shampoo:", success)
        if not success:
            return self.info

        # Step 4: Pick bread and place on tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread:", success)
        if not success:
            return self.info

        # Step 5: Pick fork and place on tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick fork:", success)
        if not success:
            return self.info

        # Step 6: Pick knife and place on tray
        success = self.pick_and_place(self.knife, self.tray)
        print("Pick knife:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - All edible items (apple, bread) and eating utensils (fork, knife) are on the tray.
        - Shampoo is not on the tray (it was mistakenly placed and then removed).
        """
        if (
            self.check_on(self.apple, self.tray) and
            self.check_on(self.bread, self.tray) and
            self.check_on(self.fork, self.tray) and
            self.check_on(self.knife, self.tray) and
            not self.check_on(self.shampoo, self.tray)
        ):
            return True
        return False
