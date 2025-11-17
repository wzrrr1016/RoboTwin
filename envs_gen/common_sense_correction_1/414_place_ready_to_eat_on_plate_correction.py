from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 414_place_ready_to_eat_on_plate_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Create the plate and edible/non-edible objects.
        - Add distractors to the environment.
        """
        # Create the plate
        self.plate = self.add_actor("plate", "plate")
        # Create edible items
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        # Create non-edible items
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        # Add distractors to the environment
        distractor_list = ["calculator", "pot-with-plant", "shoe", "book", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - Pick and place edible items on the plate.
        - Correct any wrong placements (e.g., hammer on plate).
        - Place non-edible items on the table.
        """
        # 1. Pick bread and place it on the plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Pick bread and place on plate:", success)
        if not success:
            return self.info

        # 2. Pick hammer and place it on the plate (wrong action)
        success = self.pick_and_place(self.hammer, self.plate)
        print("Pick hammer and place on plate (wrong):", success)
        if not success:
            return self.info

        # 3. Recover: pick hammer from plate and place it on the table
        success = self.pick_and_place(self.hammer, self.table)
        print("Recover hammer and place on table:", success)
        if not success:
            return self.info

        # 4. Pick hamburg and place it on the plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Pick hamburg and place on plate:", success)
        if not success:
            return self.info

        # 5. Pick screwdriver and place it on the table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Pick screwdriver and place on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Edible items (bread, hamburg) must be on the plate.
        - Non-edible items (hammer, screwdriver) must not be on the plate.
        """
        # Check if edible items are on the plate
        bread_on_plate = self.check_on(self.bread, self.plate)
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)

        # Check if non-edible items are not on the plate
        hammer_not_on_plate = not self.check_on(self.hammer, self.plate)
        screwdriver_not_on_plate = not self.check_on(self.screwdriver, self.plate)

        # Return True only if all conditions are met
        return bread_on_plate and hamburg_on_plate and hammer_not_on_plate and screwdriver_not_on_plate
