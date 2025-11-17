from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 281_food_vs_tools_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers and objects specified in the task.
        Distractors are also added to simulate a realistic environment.
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.tray = self.add_actor("tray", "tray")

        # Add objects to be manipulated
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.knife = self.add_actor("knife", "knife")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.blue_block = self.add_actor("blue_block", "blue_block")

        # Add distractors to the environment
        distractor_list = ["calculator", "pot-with-plant", "shoe", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        This includes both correct and recovery actions as specified in the task.
        """
        # Step 1: Wrong action - Place apple into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick apple to fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery action - Move apple from fluted_block to tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Pick apple to tray (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place french_fries into tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Pick french_fries to tray:", success)
        if not success:
            return self.info

        # Step 4: Place knife into fluted_block
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Pick knife to fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell into fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Pick dumbbell to fluted_block:", success)
        if not success:
            return self.info

        # Step 6: Place blue_block into fluted_block
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Pick blue_block to fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        This includes verifying the correct placement of all objects.
        """
        # Check if apple and french_fries are on the tray
        # Check if knife, dumbbell, and blue_block are in the fluted_block
        if (self.check_on(self.apple, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.knife, self.fluted_block) and
            self.check_on(self.dumbbell, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block)):
            return True
        return False
