from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 423_place_ready_to_eat_on_plate_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes the plate, ready-to-eat foods, tools, electronics, and distractors.
        """
        # Add the plate as a container
        self.plate = self.add_actor("plate", "plate")
        
        # Add ready-to-eat foods
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add tools and electronics
        self.knife = self.add_actor("knife", "knife")
        self.microphone = self.add_actor("microphone", "microphone")
        
        # Add distractor objects
        distractors = ["pot-with-plant", "shoe", "book", "toycar", "tissue-box"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Place bread on the plate
        2. Place hamburg on the plate
        3. Place knife on the plate (wrong action)
        4. Recover by placing knife on the table
        5. Place microphone on the table
        """
        # Place bread on the plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Place bread on plate:", success)
        if not success:
            return self.info

        # Place hamburg on the plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Place hamburg on plate:", success)
        if not success:
            return self.info

        # Wrong action: Place knife on the plate
        success = self.pick_and_place(self.knife, self.plate)
        print("Place knife on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: Place knife on the table
        success = self.pick_and_place(self.knife, self.table)
        print("Recover knife to table:", success)
        if not success:
            return self.info

        # Place microphone on the table
        success = self.pick_and_place(self.microphone, self.table)
        print("Place microphone on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Ready-to-eat foods (bread, hamburg) are on the plate
        - Tools (knife) and electronics (microphone) are NOT on the plate
        """
        # Check if ready-to-eat foods are on the plate
        bread_on_plate = self.check_on(self.bread, self.plate)
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)
        
        # Check if tools and electronics are NOT on the plate
        knife_not_on_plate = not self.check_on(self.knife, self.plate)
        microphone_not_on_plate = not self.check_on(self.microphone, self.plate)
        
        # Return True only if all conditions are met
        return all([
            bread_on_plate,
            hamburg_on_plate,
            knife_not_on_plate,
            microphone_not_on_plate
        ])
