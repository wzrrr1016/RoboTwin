from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 42_coaster_suitable_placement_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the coaster as a container.
        - Add the relevant objects (bottle, sand-clock, apple, bread).
        - Add distractor objects to the environment.
        """
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add the main objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects
        distractors = ["calculator", "screwdriver", "battery", "hammer", "shoe"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Execute the robot's sequence of actions to complete the task:
        1. Place apple on coaster (wrong action)
        2. Place apple back on table (recovery)
        3. Place bottle on coaster
        4. Place sand-clock on coaster
        5. Place bread back on table
        """
        # Step 1: Place apple on coaster (wrong action)
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 2: Place apple back on table (recovery)
        success = self.pick_and_place(self.apple, self.table)
        print("Place apple on table (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place bottle on coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Place bottle on coaster:", success)
        if not success:
            return self.info

        # Step 4: Place sand-clock on coaster
        success = self.pick_and_place(self.sand_clock, self.coaster)
        print("Place sand-clock on coaster:", success)
        if not success:
            return self.info

        # Step 5: Place bread back on table
        success = self.pick_and_place(self.bread, self.table)
        print("Place bread on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Bottle and sand-clock are on the coaster
        - Apple and bread are not on the coaster
        """
        # Check if bottle and sand-clock are on the coaster
        bottle_on_coaster = self.check_on(self.bottle, self.coaster)
        sand_clock_on_coaster = self.check_on(self.sand_clock, self.coaster)
        
        # Check if apple and bread are not on the coaster
        apple_not_on_coaster = not self.check_on(self.apple, self.coaster)
        bread_not_on_coaster = not self.check_on(self.bread, self.coaster)
        
        # Return True if all conditions are met
        return all([
            bottle_on_coaster,
            sand_clock_on_coaster,
            apple_not_on_coaster,
            bread_not_on_coaster
        ])
