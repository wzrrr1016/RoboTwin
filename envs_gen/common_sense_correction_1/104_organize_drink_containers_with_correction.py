from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 104_organize_drink_containers_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        - Containers: fluted_block
        - Objects: bottle, cup, can, hamburg
        - Distractors: calculator, screwdriver, toycar, shoe, book
        """
        # Create the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create drink containers (reusable/disposable)
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup = self.add_actor("cup", "cup")
        self.can = self.add_actor("can", "can")
        
        # Create food item to leave on table
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "screwdriver", "toycar", "shoe", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the environment:
        1. Place bottle in organizer
        2. (Wrong) Place hamburg in organizer
        3. Recover hamburg and place on table
        4. Place cup in organizer
        5. Place can in organizer
        """
        # Place bottle in organizer
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle:", success)
        if not success:
            return self.info

        # (Wrong) Place hamburg in organizer
        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("Place hamburg (wrong):", success)
        if not success:
            return self.info

        # Recover hamburg and place on table
        success = self.pick_and_place(self.hamburg, self.table)
        print("Recover hamburg:", success)
        if not success:
            return self.info

        # Place cup in organizer
        success = self.pick_and_place(self.cup, self.fluted_block)
        print("Place cup:", success)
        if not success:
            return self.info

        # Place can in organizer
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Place can:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - All drink containers (bottle, cup, can) are in the organizer
        - Food item (hamburg) remains on the table
        """
        # Check if all drink containers are in the organizer
        drink_containers_in_organizer = (
            self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.cup, self.fluted_block) and
            self.check_on(self.can, self.fluted_block)
        )
        
        # Check if food item is on the table
        food_on_table = self.check_on(self.hamburg, self.table)
        
        # Return True only if all conditions are met
        return drink_containers_in_organizer and food_on_table
