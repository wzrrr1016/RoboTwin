from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 140_place_drink_containers_on_coaster_with_one_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        - Containers: coaster
        - Objects: bottle, can, french_fries, tissue-box
        - Distractors: calculator, screwdriver, pot-with-plant, shoe, book
        """
        # Create the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Create the main objects for the task
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects to the environment
        distractors = ["calculator", "screwdriver", "pot-with-plant", "shoe", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Place drinkable containers (bottle and can) on the coaster
        2. Place snack (french fries) on coaster (wrong action), then recover by moving to table
        3. Place disposable item (tissue box) on table
        """
        # Place bottle on coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Pick bottle and place on coaster:", success)
        if not success:
            return self.info

        # Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Pick can and place on coaster:", success)
        if not success:
            return self.info

        # Wrong action: place french fries on coaster
        success = self.pick_and_place(self.french_fries, self.coaster)
        print("Pick french fries and place on coaster (wrong):", success)
        if not success:
            return self.info

        # Recovery: move french fries to table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Pick french fries and place on table (recovery):", success)
        if not success:
            return self.info

        # Place tissue box on table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Pick tissue-box and place on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Drinkable containers (bottle and can) are on the coaster
        - Snack (french fries) and disposable item (tissue box) are NOT on the coaster
        """
        success_conditions = (
            self.check_on(self.bottle, self.coaster) and
            self.check_on(self.can, self.coaster) and
            not self.check_on(self.french_fries, self.coaster) and
            not self.check_on(self.tissue_box, self.coaster)
        )
        
        return success_conditions
