from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 210_hygiene_recyclable_on_tray_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Adds the tray as the main container.
        - Adds hygiene items (shampoo, tissue-box), recyclable containers (can),
          hot/oily food (french_fries), and tools (screwdriver).
        - Adds distractor objects as specified in the task description.
        """
        # Add the tray as the main container
        self.tray = self.add_actor("tray", "tray")

        # Add hygiene items and small recyclable containers
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.can = self.add_actor("can", "can")

        # Add hot/oily food and tools
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractor objects
        distractor_list = ['book', 'shoe', 'pot-with-plant', 'toycar', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Place hygiene items and small recyclable containers on the tray.
        - Place hot/oily food and tools on the table.
        - If any action fails, the task is terminated early.
        """
        # Place shampoo on the tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Place shampoo on tray:", success)
        if not success:
            return self.info

        # Place tissue-box on the tray
        success = self.pick_and_place(self.tissue_box, self.tray)
        print("Place tissue-box on tray:", success)
        if not success:
            return self.info

        # Place can on the tray
        success = self.pick_and_place(self.can, self.tray)
        print("Place can on tray:", success)
        if not success:
            return self.info

        # Wrongly place french_fries on the tray (recovery step needed)
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Wrongly place french_fries on tray:", success)
        if not success:
            return self.info

        # Recover by placing french_fries on the table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Recover french_fries to table:", success)
        if not success:
            return self.info

        # Place screwdriver on the table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Place screwdriver on table:", success)
        if not success:
            return self.info

        return self.info  # Task completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Hygiene items and small recyclable containers must be on the tray.
        - Hot/oily food and tools must be on the table (not on the tray).
        """
        # Check if hygiene items and can are on the tray
        on_tray = (
            self.check_on(self.shampoo, self.tray) and
            self.check_on(self.tissue_box, self.tray) and
            self.check_on(self.can, self.tray)
        )

        # Check if hot/oily food and tools are on the table
        on_table = (
            self.check_on(self.french_fries, self.table) and
            self.check_on(self.screwdriver, self.table)
        )

        return on_tray and on_table
