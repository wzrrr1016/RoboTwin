from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 490_place_consumable_and_personal_care_items(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Containers: fluted_block
        - Objects: shampoo, mug, apple, pot-with-plant
        - Distractors: calculator, screwdriver, hammer, toycar, alarm-clock
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the target objects
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.mug = self.add_actor("mug", "mug")
        self.apple = self.add_actor("apple", "apple")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractors
        distractors = ["calculator", "screwdriver", "hammer", "toycar", "alarm-clock"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - Pick and place apple into fluted_block
        - Pick and place shampoo into fluted_block
        - Pick and place pot-with-plant into fluted_block (wrong action)
        - Recover by picking pot-with-plant from fluted_block and placing it on the table
        - Pick and place mug into fluted_block
        """
        # Pick and place apple
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick and place apple:", success)
        if not success:
            return self.info

        # Pick and place shampoo
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Pick and place shampoo:", success)
        if not success:
            return self.info

        # Wrongly place pot-with-plant
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Pick and place pot-with-plant (wrong):", success)
        if not success:
            return self.info

        # Recover by placing pot-with-plant on the table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Recover pot-with-plant to table:", success)
        if not success:
            return self.info

        # Pick and place mug
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Pick and place mug:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed.
        - Apple, shampoo, and mug must be on the fluted_block
        - Pot-with-plant must not be on the fluted_block
        """
        apple_on = self.check_on(self.apple, self.fluted_block)
        shampoo_on = self.check_on(self.shampoo, self.fluted_block)
        mug_on = self.check_on(self.mug, self.fluted_block)
        pot_not_in = not self.check_on(self.pot_with_plant, self.fluted_block)

        return apple_on and shampoo_on and mug_on and pot_not_in
