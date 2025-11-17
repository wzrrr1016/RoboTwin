from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 125_collect_colorful_square_toys_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Adds the tray as the target container.
        - Adds the colorful square toys (red_block, pink_block, yellow_block).
        - Adds the fork (used in a wrong action and recovery).
        - Adds distractor objects to the environment.
        """
        # Add the tray as the target container
        self.tray = self.add_actor("tray", "tray")

        # Add the colorful square toys
        self.red_block = self.add_actor("red_block", "red_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add the fork (used in a wrong action and recovery)
        self.fork = self.add_actor("fork", "fork")

        # Add distractor objects to the environment
        distractors = ["calculator", "pot-with-plant", "shoe", "hammer", "microphone"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - Pick and place red_block on the tray.
        - Pick and place pink_block on the tray.
        - Pick and place fork on the tray (wrong action).
        - Pick and place fork on the table (recovery).
        - Pick and place yellow_block on the tray.
        """
        # Pick and place red_block on the tray
        success = self.pick_and_place(self.red_block, self.tray)
        print("Pick red_block:", success)
        if not success:
            return self.info

        # Pick and place pink_block on the tray
        success = self.pick_and_place(self.pink_block, self.tray)
        print("Pick pink_block:", success)
        if not success:
            return self.info

        # Pick and place fork on the tray (wrong action)
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick fork (wrong):", success)
        if not success:
            return self.info

        # Pick and place fork on the table (recovery)
        success = self.pick_and_place(self.fork, self.table)
        print("Recover fork to table:", success)
        if not success:
            return self.info

        # Pick and place yellow_block on the tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Pick yellow_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All colorful square toys (red_block, pink_block, yellow_block) must be on the tray.
        - The fork must be on the table (not on the tray).
        """
        if (
            self.check_on(self.red_block, self.tray) and
            self.check_on(self.pink_block, self.tray) and
            self.check_on(self.yellow_block, self.tray) and
            self.check_on(self.fork, self.table)
        ):
            return True
        return False
