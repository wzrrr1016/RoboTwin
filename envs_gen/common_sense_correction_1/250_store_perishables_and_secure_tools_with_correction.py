from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 250_store_perishables_and_secure_tools_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        Adds the wooden_box and fluted_block as containers.
        Adds the apple, bread, pot-with-plant, and knife as objects.
        Adds distractors as specified in the task description.
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors
        distractor_list = ["calculator", "toycar", "alarm-clock", "book", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        1. Place the pot-with-plant into the wooden_box (wrong action).
        2. Recover by moving the pot-with-plant to the fluted_block.
        3. Place the apple, bread, and knife into the wooden_box.
        """
        # Step 1: Wrong placement of pot-with-plant into wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Wrong placement of pot-with-plant:", success)
        if not success:
            return self.info

        # Step 2: Recovery - move pot-with-plant to fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Recovery of pot-with-plant:", success)
        if not success:
            return self.info

        # Step 3: Place apple into wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Place apple:", success)
        if not success:
            return self.info

        # Step 4: Place bread into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread:", success)
        if not success:
            return self.info

        # Step 5: Place knife into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Place knife:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The task is successful if:
        - Apple is in the wooden_box
        - Bread is in the wooden_box
        - Knife is in the wooden_box
        - Pot-with-plant is on the fluted_block
        """
        return (
            self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.bread, self.wooden_box) and
            self.check_on(self.knife, self.wooden_box) and
            self.check_on(self.pot_with_plant, self.fluted_block)
        )
