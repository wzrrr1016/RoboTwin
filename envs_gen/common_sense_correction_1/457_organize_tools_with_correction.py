from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 457_organize_tools_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Adds the tray as the container.
        - Adds the required objects: hammer, mug, screwdriver, stapler, tissue-box.
        - Adds distractor objects as specified in the task description.
        """
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")

        # Add required objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.mug = self.add_actor("mug", "mug")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.stapler = self.add_actor("stapler", "stapler")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")

        # Add distractor objects
        distractor_list = ["toycar", "shoe", "pot-with-plant", "apple", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - Pick and place the hammer, screwdriver, and stapler onto the tray.
        - Place the mug on the tray (wrong action), then recover by placing it on the table.
        - Place the tissue-box on the table.
        """
        # Place hammer on tray
        success = self.pick_and_place(self.hammer, self.tray)
        print("Hammer placed on tray:", success)
        if not success:
            return self.info

        # Place screwdriver on tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Screwdriver placed on tray:", success)
        if not success:
            return self.info

        # Wrongly place mug on tray
        success = self.pick_and_place(self.mug, self.tray)
        print("Mug placed on tray (wrong):", success)
        if not success:
            return self.info

        # Recovery: move mug to table
        success = self.pick_and_place(self.mug, self.table)
        print("Mug moved to table:", success)
        if not success:
            return self.info

        # Place stapler on tray
        success = self.pick_and_place(self.stapler, self.tray)
        print("Stapler placed on tray:", success)
        if not success:
            return self.info

        # Place tissue-box on table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Tissue-box moved to table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All reusable tools (hammer, screwdriver, stapler) are on the tray.
        - Fragile drinkware (mug) and disposable hygiene item (tissue-box) are on the table.
        """
        if (
            self.check_on(self.hammer, self.tray) and
            self.check_on(self.screwdriver, self.tray) and
            self.check_on(self.stapler, self.tray) and
            self.check_on(self.mug, self.table) and
            self.check_on(self.tissue_box, self.table)
        ):
            return True
        return False
