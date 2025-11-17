from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 105_place_edible_items_on_plate_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Containers: plate
        - Objects: bread, hamburg, toycar, knife
        - Distractors: calculator, pot-with-plant, alarm-clock, shoe, book, microphone
        """
        # Add the plate as a container
        self.plate = self.add_actor("plate", "plate")
        
        # Add edible objects
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add non-edible objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractors to the environment
        distractors = ["calculator", "pot-with-plant", "alarm-clock", "shoe", "book", "microphone"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - First, place the toy car on the plate (wrong action).
        - Then, recover by placing the toy car back on the table.
        - Place edible items (bread and hamburg) on the plate.
        - Place the knife (sharp tool) on the table.
        """
        # Wrong action: place toycar on plate
        success = self.pick_and_place(self.toycar, self.plate)
        print("Pick toycar and place into plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: move toycar back to table
        success = self.pick_and_place(self.toycar, self.table)
        print("Pick toycar from plate and place on table (recovery):", success)
        if not success:
            return self.info

        # Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Pick bread and place into plate:", success)
        if not success:
            return self.info

        # Place hamburg on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Pick hamburg and place into plate:", success)
        if not success:
            return self.info

        # Place knife on table
        success = self.pick_and_place(self.knife, self.table)
        print("Pick knife and place on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed.
        - Bread and hamburg must be on the plate.
        - Toy car and knife must not be on the plate.
        """
        # Check if edible items are on the plate
        bread_on_plate = self.check_on(self.bread, self.plate)
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)

        # Check if non-edible items are not on the plate
        toycar_not_on_plate = not self.check_on(self.toycar, self.plate)
        knife_not_on_plate = not self.check_on(self.knife, self.plate)

        # Return True only if all conditions are met
        return bread_on_plate and hamburg_on_plate and toycar_not_on_plate and knife_not_on_plate
