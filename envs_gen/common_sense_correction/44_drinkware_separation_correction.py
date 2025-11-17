from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 44_drinkware_separation_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the environment.
        - Add containers: coaster and fluted_block.
        - Add objects: can, mug, knife, bell, bread.
        - Add distractors: calculator, pet-collar, table-tennis, battery, screwdriver.
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.can = self.add_actor("can", "can")
        self.mug = self.add_actor("mug", "mug")
        self.knife = self.add_actor("knife", "knife")
        self.bell = self.add_actor("bell", "bell")
        self.bread = self.add_actor("bread", "bread")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "table-tennis", "battery", "screwdriver"]
        self.add_distractors(distractor_list)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - First, place the can into the fluted_block (wrong action).
        - Then, recover by placing the can into the coaster.
        - Place the mug into the coaster.
        - Place the knife, bell, and bread into the fluted_block.
        """
        # Wrong placement of can
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Wrong placement can:", success)
        if not success:
            return self.info

        # Recovery: move can to coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Recovery can:", success)
        if not success:
            return self.info

        # Place mug into coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Mug to coaster:", success)
        if not success:
            return self.info

        # Place knife into fluted_block
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Knife to fluted_block:", success)
        if not success:
            return self.info

        # Place bell into fluted_block
        success = self.pick_and_place(self.bell, self.fluted_block)
        print("Bell to fluted_block:", success)
        if not success:
            return self.info

        # Place bread into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Bread to fluted_block:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Drinkware (can, mug) must be on the coaster.
        - Non-drinkware (knife, bell, bread) must be on the fluted_block.
        """
        if (self.check_on(self.can, self.coaster) and
            self.check_on(self.mug, self.coaster) and
            self.check_on(self.knife, self.fluted_block) and
            self.check_on(self.bell, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block)):
            return True
        return False
