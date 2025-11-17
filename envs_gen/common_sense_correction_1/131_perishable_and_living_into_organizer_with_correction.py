from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 131_perishable_and_living_into_organizer_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: fluted_block
        - Objects: bread, pot-with-plant, green_block, bottle, yellow_block
        - Distractors: calculator, stapler, microphone, shoe, alarm-clock
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the main objects
        self.bread = self.add_actor("bread", "bread")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.green_block = self.add_actor("green_block", "green_block")
        self.bottle = self.add_actor("bottle", "bottle")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors
        distractor_list = ["calculator", "stapler", "microphone", "shoe", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Place green_block into fluted_block (wrong action)
        2. Recover green_block to table
        3. Place bread into fluted_block
        4. Place pot-with-plant into fluted_block
        5. Place bottle on table
        6. Place yellow_block on table
        """
        # Step 1: Wrong action - place green_block into fluted_block
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block into fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Recovery - place green_block back on table
        success = self.pick_and_place(self.green_block, self.table)
        print("Recover green_block to table:", success)
        if not success:
            return self.info

        # Step 3: Place bread into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread into fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Place pot-with-plant into fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Place pot-with-plant into fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place bottle on table
        success = self.pick_and_place(self.bottle, self.table)
        print("Place bottle on table:", success)
        if not success:
            return self.info

        # Step 6: Place yellow_block on table
        success = self.pick_and_place(self.yellow_block, self.table)
        print("Place yellow_block on table:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Verify that the task was completed successfully:
        - Perishable/living items (bread, pot-with-plant) are in fluted_block
        - Non-perishable items (green_block, bottle, yellow_block) are on the table
        """
        return (
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.pot_with_plant, self.fluted_block) and
            self.check_on(self.green_block, self.table) and
            self.check_on(self.bottle, self.table) and
            self.check_on(self.yellow_block, self.table)
        )
