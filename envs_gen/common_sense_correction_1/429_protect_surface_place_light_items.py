from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 429_protect_surface_place_light_items(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")

        # Add the main objects involved in the task
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.teanet = self.add_actor("teanet", "teanet")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractor objects to the environment
        distractor_list = ["calculator", "pot-with-plant", "alarm-clock", "book", "battery"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions to complete the task.
        """
        # Step 1: Place the pink block on the coaster
        success = self.pick_and_place(self.pink_block, self.coaster)
        print("Pick and place pink_block:", success)
        if not success:
            return self.info

        # Step 2: Place the blue block on the coaster
        success = self.pick_and_place(self.blue_block, self.coaster)
        print("Pick and place blue_block:", success)
        if not success:
            return self.info

        # Step 3: (Wrong action) Place the dumbbell on the coaster
        success = self.pick_and_place(self.dumbbell, self.coaster)
        print("Pick and place dumbbell (wrong):", success)
        if not success:
            return self.info

        # Step 4: (Recovery) Move the dumbbell from the coaster to the table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick and place dumbbell to table:", success)
        if not success:
            return self.info

        # Step 5: Place the teanet on the coaster
        success = self.pick_and_place(self.teanet, self.coaster)
        print("Pick and place teanet:", success)
        if not success:
            return self.info

        return self.info  # All actions completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Lightweight toys and small kitchen utensils are on the coaster.
        - Heavy exercise equipment is not on the coaster.
        """
        # Check if pink_block, blue_block, and teanet are on the coaster
        if (
            self.check_on(self.pink_block, self.coaster) and
            self.check_on(self.blue_block, self.coaster) and
            self.check_on(self.teanet, self.coaster)
        ):
            # Check if the dumbbell is NOT on the coaster
            if not self.check_on(self.dumbbell, self.coaster):
                return True
        return False
