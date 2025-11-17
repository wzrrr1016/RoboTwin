from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 409_collect_small_portable_items_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load the main actors (objects and containers) into the simulation environment.
        Distractors are also added to simulate a realistic cluttered scene.
        """
        # Add the tray as the main container
        self.tray = self.add_actor("tray", "tray")

        # Add the target objects to be placed on the tray
        self.toycar = self.add_actor("toycar", "toycar")
        self.green_block = self.add_actor("green_block", "green_block")
        self.mouse = self.add_actor("mouse", "mouse")
        self.cup = self.add_actor("cup", "cup")

        # Add distractors to the environment
        distractor_list = ['pot-with-plant', 'baguette', 'tissue-box', 'roll-paper', 'apple']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The robot will:
        1. Pick toycar and place it on the tray
        2. Pick cup and place it on the tray
        3. Pick green_block and place it on the table (wrong action)
        4. Pick green_block from the table and place it on the tray (recovery)
        5. Pick mouse and place it on the tray
        """
        # Step 1: Place toycar on tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Pick toycar and place on tray:", success)
        if not success:
            return self.info

        # Step 2: Place cup on tray
        success = self.pick_and_place(self.cup, self.tray)
        print("Pick cup and place on tray:", success)
        if not success:
            return self.info

        # Step 3: Place green_block on table (wrong action)
        success = self.pick_and_place(self.green_block, self.table)
        print("Pick green_block and place on table (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover green_block and place on tray
        success = self.pick_and_place(self.green_block, self.tray)
        print("Pick green_block from table and place on tray (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place mouse on tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("Pick mouse and place on tray:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if all target objects are on the tray to confirm task completion.
        """
        return (
            self.check_on(self.toycar, self.tray) and
            self.check_on(self.cup, self.tray) and
            self.check_on(self.green_block, self.tray) and
            self.check_on(self.mouse, self.tray)
        )
