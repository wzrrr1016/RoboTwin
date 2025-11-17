from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 483_place_liquid_bottles_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add the main objects for the task
        self.bottle = self.add_actor("bottle", "bottle")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.fork = self.add_actor("fork", "fork")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "toycar", "alarm-clock", "shoe", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation environment.
        This includes both correct actions and error recovery.
        """
        # Place liquid-holding bottles on the coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Place bottle on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Place shampoo on coaster:", success)
        if not success:
            return self.info

        # Wrong action: Place fork on coaster (incorrect placement)
        success = self.pick_and_place(self.fork, self.coaster)
        print("Wrong: Place fork on coaster:", success)
        if not success:
            return self.info

        # Recovery action: Move fork back to table
        success = self.pick_and_place(self.fork, self.table)
        print("Recovery: Place fork on table:", success)
        if not success:
            return self.info

        # Place food on the table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Place french fries on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking object placements.
        """
        # Check if liquid-holding bottles are on the coaster
        liquid_on_coaster = (
            self.check_on(self.bottle, self.coaster) and 
            self.check_on(self.shampoo, self.coaster)
        )
        
        # Check if food and utensils are on the table
        food_utensils_on_table = (
            self.check_on(self.fork, self.table) and 
            self.check_on(self.french_fries, self.table)
        )
        
        # Return True if all conditions are met
        return liquid_on_coaster and food_utensils_on_table
