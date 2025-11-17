from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 320_organize_solids_and_dispose_perishables_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Containers: fluted_block, dustbin
        - Objects: screwdriver, apple, blue_block, yellow_block, shampoo
        - Distractors: calculator, book, shoe, alarm-clock, pot-with-plant
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.apple = self.add_actor("apple", "apple")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.shampoo = self.add_actor("shampoo", "shampoo")

        # Add distractors
        distractor_list = ["calculator", "book", "shoe", "alarm-clock", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Actions:
        1. Place screwdriver into fluted_block
        2. Place blue_block into fluted_block
        3. Place apple into fluted_block (wrong action)
        4. Recover apple by placing it into dustbin
        5. Place yellow_block into fluted_block
        6. Place shampoo into dustbin
        """
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple (wrong):", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.apple, self.dustbin)
        print("Recover apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Place shampoo:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Solid toys and handy tools (screwdriver, blue_block, yellow_block) are in fluted_block
        - Perishable foods and liquid personal-care items (apple, shampoo) are in dustbin
        """
        if (
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block) and
            self.check_on(self.apple, self.dustbin) and
            self.check_on(self.shampoo, self.dustbin)
        ):
            return True
        return False
