from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 305_place_food_and_utensils_on_plate_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Containers: plate
        - Objects: bread, mug, fork, toycar
        - Distractors: calculator, screwdriver, shoe, book, alarm-clock
        """
        # Add the plate as a container
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects that need to be placed on the plate
        self.bread = self.add_actor("bread", "bread")
        self.mug = self.add_actor("mug", "mug")
        self.fork = self.add_actor("fork", "fork")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractor objects to the environment
        distractors = ['calculator', 'screwdriver', 'shoe', 'book', 'alarm-clock']
        self.add_distractors(distractors)

    def play_once(self):
        """
        Execute the robot's actions in the simulation environment.
        Steps:
        1. Pick toycar and place it onto plate (wrong action)
        2. Pick toycar from plate and place it on table (recovery)
        3. Pick bread and place it onto plate
        4. Pick mug and place it onto plate
        5. Pick fork and place it onto plate
        """
        # Step 1: Wrong placement of toycar
        success = self.pick_and_place(self.toycar, self.plate)
        print("Pick toycar and place onto plate (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery of toycar
        success = self.pick_and_place(self.toycar, self.table)
        print("Pick toycar from plate and place it on table (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Pick bread and place onto plate:", success)
        if not success:
            return self.info

        # Step 4: Place mug on plate
        success = self.pick_and_place(self.mug, self.plate)
        print("Pick mug and place onto plate:", success)
        if not success:
            return self.info

        # Step 5: Place fork on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Pick fork and place onto plate:", success)
        if not success:
            return self.info

        return self.info  # All actions completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully.
        Success criteria:
        - Bread, mug, and fork are on the plate
        - Toycar is not on the plate (must have been recovered)
        """
        if (self.check_on(self.bread, self.plate) and
            self.check_on(self.mug, self.plate) and
            self.check_on(self.fork, self.plate) and
            not self.check_on(self.toycar, self.plate)):
            return True
        return False
