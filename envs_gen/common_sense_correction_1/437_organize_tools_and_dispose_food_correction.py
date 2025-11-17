from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 437_organize_tools_and_dispose_food_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        Includes:
        - Containers: fluted_block (organizer surface), dustbin
        - Objects: screwdriver, drill, knife, french_fries
        - Distractors: calculator, alarm-clock, toycar, book, pot-with-plant
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add task-relevant objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.drill = self.add_actor("drill", "drill")
        self.knife = self.add_actor("knife", "knife")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractors
        distractor_list = ["calculator", "alarm-clock", "toycar", "book", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's sequence of actions:
        1. Place maintenance tools (screwdriver, drill) on fluted_block
        2. Place knife on fluted_block
        3. Place french_fries on fluted_block (wrong action)
        4. Recover by moving french_fries to dustbin
        """
        # Place maintenance tools on organizer surface
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Place drill:", success)
        if not success:
            return self.info

        # Place knife on organizer surface
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Place knife:", success)
        if not success:
            return self.info

        # Place french_fries on fluted_block (wrong action)
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french fries (wrong):", success)
        if not success:
            return self.info

        # Recover by placing french_fries in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Dispose of french fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Maintenance tools (screwdriver, drill) and sharp utensil (knife) are on fluted_block
        - Fast food (french_fries) is in the dustbin
        """
        if (self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.drill, self.fluted_block) and
            self.check_on(self.knife, self.fluted_block) and
            self.check_on(self.french_fries, self.dustbin)):
            return True
        return False
