from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 80_store_toys_and_tools_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: fluted_block, shoe_box
        - Objects: blue_block, yellow_block, pot-with-plant, drill, hamburg
        - Distractors: calculator, book, alarm-clock, small-speaker, mouse
        """
        # Create containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Create objects to be manipulated
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.drill = self.add_actor("drill", "drill")
        self.hamburg = self.add_actor("hamburg", "hamburg")

        # Add distractors to the environment
        distractor_list = ["calculator", "book", "alarm-clock", "small-speaker", "mouse"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot:
        1. Places blue_block into fluted_block
        2. Incorrectly places drill into fluted_block (wrong action)
        3. Recovers by placing drill into shoe_box
        4. Places yellow_block, pot-with-plant, and hamburg into fluted_block
        """
        # Step 1: Place blue_block into fluted_block
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # Step 2: Place drill into fluted_block (wrong action)
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Place drill (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing drill into shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Recover drill to shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Place yellow_block into fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        # Step 5: Place pot-with-plant into fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Place pot-with-plant:", success)
        if not success:
            return self.info

        # Step 6: Place hamburg into fluted_block
        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("Place hamburg:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the final state of the simulation meets the task requirements:
        - Small toys and delicate living or edible items (blue_block, yellow_block, pot-with-plant, hamburg) are in fluted_block
        - Tools and heavy objects (drill) are in shoe_box
        """
        if (
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block) and
            self.check_on(self.pot_with_plant, self.fluted_block) and
            self.check_on(self.hamburg, self.fluted_block) and
            self.check_on(self.drill, self.shoe_box)
        ):
            return True
        return False
