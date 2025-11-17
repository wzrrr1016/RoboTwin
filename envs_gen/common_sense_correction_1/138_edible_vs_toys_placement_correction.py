from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 138_edible_vs_toys_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Adds the tray and fluted_block as containers, and the relevant objects.
        Adds distractors to the environment.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.toycar = self.add_actor("toycar", "toycar")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.green_block = self.add_actor("green_block", "green_block")

        # Add distractors
        distractor_list = ["screwdriver", "hammer", "shampoo", "alarm-clock", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        Includes a wrong initial placement and a recovery step.
        """
        # Step 1: Wrong placement of bread into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Pick bread and place into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - move bread to tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Recover: Pick bread and place into tray:", success)
        if not success:
            return self.info

        # Step 3: Place french_fries on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french_fries on tray:", success)
        if not success:
            return self.info

        # Step 4: Place toycar on fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar on fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place yellow_block on fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Place yellow_block on fluted_block:", success)
        if not success:
            return self.info

        # Step 6: Place green_block on fluted_block
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block on fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        Verifies that edible items are on the tray and children's toys are on the fluted_block.
        """
        return (
            self.check_on(self.bread, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block) and
            self.check_on(self.green_block, self.fluted_block)
        )
