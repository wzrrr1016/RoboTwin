from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 269_fast_food_plate_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Create the plate container
        - Create fast-food items (hamburg, french_fries)
        - Create non-fast-food items (bread, cup)
        - Add distractor objects to the environment
        """
        # Create the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Create fast-food items
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Create non-fast-food items
        self.bread = self.add_actor("bread", "bread")
        self.cup = self.add_actor("cup", "cup")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "screwdriver", "alarm-clock", "toycar", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot actions:
        1. Place hamburg on plate
        2. Place french_fries on plate
        3. Wrongly place bread on plate (then recover)
        4. Place cup on table
        """
        # Place hamburg on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Place hamburg:", success)
        if not success:
            return self.info

        # Place french_fries on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries:", success)
        if not success:
            return self.info

        # Wrongly place bread on plate (this will be corrected)
        success = self.pick_and_place(self.bread, self.plate)
        print("Wrongly place bread:", success)
        if not success:
            return self.info

        # Recover: Move bread from plate to table
        success = self.pick_and_place(self.bread, self.table)
        print("Recover bread:", success)
        if not success:
            return self.info

        # Place cup on table
        success = self.pick_and_place(self.cup, self.table)
        print("Place cup:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - hamburg and french_fries are on the plate
        - bread and cup are not on the plate
        """
        # Check that fast-food items are on the plate
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)
        french_fries_on_plate = self.check_on(self.french_fries, self.plate)
        
        # Check that non-fast-food items are not on the plate
        bread_not_on_plate = not self.check_on(self.bread, self.plate)
        cup_not_on_plate = not self.check_on(self.cup, self.plate)
        
        # Return True if all conditions are met
        return (hamburg_on_plate and french_fries_on_plate and 
                bread_not_on_plate and cup_not_on_plate)
