from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 16_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the main container (plate)
        self.plate = self.add_actor("plate", "plate")
        
        # Add drinkware and tools
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.bottle = self.add_actor("bottle", "bottle")
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractors to the scene
        distractor_list = ['pet-collar', 'table-tennis', 'pot-with-plant', 
                          'alarm-clock', 'shoe', 'book']
        self.add_distractors(distractor_list)
        
        # Final scene validation
        self.check_scene()

    def play_once(self):
        """
        Execute the sequence of robot arm actions to complete the task.
        """
        # Step 1: Place cup_with_handle into plate
        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Cup with handle placement:", success)
        if not success:
            return self.info

        # Step 2: Place bottle into plate
        success = self.pick_and_place(self.bottle, self.plate)
        print("Bottle placement:", success)
        if not success:
            return self.info

        # Step 3: (Wrong action) Place hammer into plate
        success = self.pick_and_place(self.hammer, self.plate)
        print("Hammer (wrong) placement:", success)
        if not success:
            return self.info

        # Step 4: (Recovery) Move hammer from plate to table
        success = self.pick_and_place(self.hammer, self.table)
        print("Hammer recovery to table:", success)
        if not success:
            return self.info

        # Step 5: Place screwdriver on table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Screwdriver placement:", success)
        if not success:
            return self.info

        # Mark task completion
        self.add_end()
        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully according to the requirements.
        """
        # Check if drinkware is in the plate
        drinkware_in_plate = (
            self.check_on(self.cup_with_handle, self.plate) and 
            self.check_on(self.bottle, self.plate)
        )
        
        # Check if tools are on the table
        tools_on_table = (
            self.check_on(self.hammer, self.table) and 
            self.check_on(self.screwdriver, self.table)
        )
        
        # Return final success status
        return drinkware_in_plate and tools_on_table
