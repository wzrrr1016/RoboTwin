from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 33_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Adds the tray as the container and the relevant objects (stapler, dumbbell, pink_block, fork).
        Adds distractors to the scene as specified in the task description.
        """
        # Add the tray as the container
        self.tray = self.add_actor("tray", "tray")

        # Add the objects that need to be placed into the tray
        self.stapler = self.add_actor("stapler", "stapler")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.fork = self.add_actor("fork", "fork")

        # Add distractors to the scene
        distractor_list = ["pet-collar", "shoe", "book", "alarm-clock", "tissue-box"]
        self.add_distractors(distractor_list)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Includes placing correct tools into the tray, a wrong action, and a recovery step.
        """
        # Step 1: Pick and place stapler into tray
        success = self.pick_and_place(self.stapler, self.tray)
        print("Pick place stapler:", success)
        if not success:
            return self.info

        # Step 2: Pick and place dumbbell into tray
        success = self.pick_and_place(self.dumbbell, self.tray)
        print("Pick place dumbbell:", success)
        if not success:
            return self.info

        # Step 3: Pick and place pink_block into tray (wrong action)
        success = self.pick_and_place(self.pink_block, self.tray)
        print("Pick place pink_block (wrong):", success)
        if not success:
            return self.info

        # Step 4: Pick pink_block from tray and place it back on the table (recovery)
        success = self.pick_and_place(self.pink_block, self.table)
        print("Recover pink_block to table:", success)
        if not success:
            return self.info

        # Step 5: Pick and place fork into tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick place fork:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The task is considered successful if the stapler, dumbbell, and fork are all on the tray.
        The pink_block should not be on the tray (it was placed and then recovered).
        """
        return (
            self.check_on(self.stapler, self.tray) and
            self.check_on(self.dumbbell, self.tray) and
            self.check_on(self.fork, self.tray)
        )
