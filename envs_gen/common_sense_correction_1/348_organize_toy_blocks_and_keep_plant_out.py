from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 348_organize_toy_blocks_and_keep_plant_out(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the container, the toy blocks, the plant, and distractors.
        """
        # Add the container (organizer)
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the bright, solid toy blocks
        self.green_block = self.add_actor("green_block", "green_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add the living decorative plant
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractor objects to the environment
        distractor_list = ["calculator", "hammer", "book", "battery", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions to complete the task.
        The robot will:
        1. Place the green block into the organizer.
        2. (Wrongly) place the plant into the organizer.
        3. Recover by placing the plant on the table.
        4. Place the blue and yellow blocks into the organizer.
        """
        # Step 1: Place green block into the organizer
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green block:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place the plant into the organizer
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Wrongly place plant:", success)
        if not success:
            return self.info

        # Step 3: Recover by placing the plant on the table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Recover plant to table:", success)
        if not success:
            return self.info

        # Step 4: Place blue block into the organizer
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue block:", success)
        if not success:
            return self.info

        # Step 5: Place yellow block into the organizer
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Place yellow block:", success)
        if not success:
            return self.info

        return self.info  # All actions completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully:
        - All toy blocks are in the organizer (fluted_block)
        - The plant is on the table (not in the organizer)
        """
        if (
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block) and
            self.check_on(self.pot_with_plant, self.table)
        ):
            return True
        return False
