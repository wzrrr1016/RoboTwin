from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 357_place_food_and_utensils_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes the plate, eating-related objects, and distractors.
        """
        # Add the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects used for eating (edible and utensils)
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        
        # Add other objects that need to be placed on the table
        self.bottle = self.add_actor("bottle", "bottle")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractor objects that are not relevant to the task
        distractor_list = ["calculator", "hammer", "drill", "shoe", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the specified sequence:
        1. Place toycar on plate (wrong action)
        2. Recover by placing toycar on table
        3. Place french fries on plate
        4. Place fork on plate
        5. Place bottle on table
        """
        # Attempt to place toycar on plate (wrong action)
        self.pick_and_place(self.toycar, self.plate)
        print("Place toycar on plate (wrong): attempted")
        
        # Recover by placing toycar on table
        self.pick_and_place(self.toycar, self.table)
        print("Recover toycar to table: attempted")
        
        # Place edible item on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french fries:", success)
        if not success:
            return self.info
        
        # Place utensil on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Place fork:", success)
        if not success:
            return self.info
        
        # Place bottle on table
        success = self.pick_and_place(self.bottle, self.table)
        print("Place bottle on table:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking:
        - French fries and fork are on the plate
        - Toycar is not on the plate (was moved to table)
        - Bottle is on the table
        """
        # Check if edible and utensil are on the plate
        if (self.check_on(self.french_fries, self.plate) and 
            self.check_on(self.fork, self.plate)):
            
            # Check if toycar is not on the plate (was moved to table)
            if not self.check_on(self.toycar, self.plate):
                
                # Check if bottle is on the table
                if self.check_on(self.bottle, self.table):
                    return True
        
        return False
