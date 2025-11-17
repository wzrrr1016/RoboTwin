from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 442_food_and_tableware_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: fluted_block
        - Edible foods: apple, french_fries
        - Drink container: mug
        - Utensil: fork
        - Distractors: calculator, screwdriver, toycar, alarm-clock, shoe
        """
        # Add the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add edible ready-to-eat foods
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add drink container and utensil
        self.mug = self.add_actor("mug", "mug")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractor objects
        self.add_distractors(["calculator", "screwdriver", "toycar", "alarm-clock", "shoe"])

    def play_once(self):
        """
        Execute the sequence of robotic actions:
        1. Place apple into fluted_block
        2. Place mug into fluted_block (wrong action)
        3. Recover by placing mug on fluted_block
        4. Place french_fries into fluted_block
        5. Place fork on fluted_block
        """
        # 1. Place apple into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info

        # 2. Place mug into fluted_block (wrong action)
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug (wrong):", success)
        if not success:
            return self.info

        # 3. Recover by placing mug on fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Recover mug placement:", success)
        if not success:
            return self.info

        # 4. Place french_fries into fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french fries:", success)
        if not success:
            return self.info

        # 5. Place fork on fluted_block
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Place fork:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Edible foods (apple, french_fries) are in the organizer
        - Utensils (fork) and drink containers (mug) are on top of the organizer
        """
        # Check if all required objects are on the fluted_block
        if (self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.french_fries, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block)):
            return True
        return False
