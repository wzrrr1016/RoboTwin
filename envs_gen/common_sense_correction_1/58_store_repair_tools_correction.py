from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 58_store_repair_tools_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the shoe_box (container), repair tools (screwdriver, hammer),
        and a non-repair object (pot-with-plant). Distractors are also added.
        """
        # Add the shoe_box as a container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add the repair tools
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add the non-repair object (pot-with-plant)
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        
        # Add distractors to the environment
        distractors = ["apple", "book", "mug", "toycar", "tissue-box"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The robot will:
        1. Place the screwdriver into the shoe_box.
        2. Place the pot-with-plant into the shoe_box (wrong action).
        3. Recover by placing the pot-with-plant on the table.
        4. Place the hammer into the shoe_box.
        """
        # Step 1: Place screwdriver into shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        # Step 2: Place pot-with-plant into shoe_box (wrong action)
        success = self.pick_and_place(self.pot_with_plant, self.shoe_box)
        print("Place pot-with-plant (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing pot-with-plant on the table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Recover pot-with-plant:", success)
        if not success:
            return self.info

        # Step 4: Place hammer into shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Place hammer:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The task is considered successful if:
        - The screwdriver is on the shoe_box.
        - The hammer is on the shoe_box.
        - The pot-with-plant is not on the shoe_box.
        """
        # Check if screwdriver and hammer are on the shoe_box
        screwdriver_on = self.check_on(self.screwdriver, self.shoe_box)
        hammer_on = self.check_on(self.hammer, self.shoe_box)
        
        # Check if the pot-with-plant is not on the shoe_box
        pot_not_on = not self.check_on(self.pot_with_plant, self.shoe_box)
        
        # Return True if all conditions are met
        return screwdriver_on and hammer_on and pot_not_on
