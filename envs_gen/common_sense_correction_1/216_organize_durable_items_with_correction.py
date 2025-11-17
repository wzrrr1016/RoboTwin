from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 216_organize_durable_items_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the container (fluted_block), the target objects (drill, dumbbell, bottle, tissue-box),
        and the distractor objects.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the target objects
        self.drill = self.add_actor("drill", "drill")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.bottle = self.add_actor("bottle", "bottle")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")

        # Add distractor objects
        distractor_list = ["book", "toycar", "alarm-clock", "pot-with-plant", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot will:
        1. Place the drill on the fluted_block.
        2. Place the dumbbell on the fluted_block.
        3. (Incorrectly) place the bottle on the fluted_block.
        4. Correct the mistake by moving the bottle to the table.
        5. Place the tissue-box on the table.
        """
        # Step 1: Place the drill on the fluted_block
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Pick and place drill:", success)
        if not success:
            return self.info

        # Step 2: Place the dumbbell on the fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Pick and place dumbbell:", success)
        if not success:
            return self.info

        # Step 3: (Incorrect) Place the bottle on the fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Pick and place bottle (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery - Move the bottle to the table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle to table:", success)
        if not success:
            return self.info

        # Step 5: Place the tissue-box on the table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Pick and place tissue-box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The success condition is:
        - Drill and dumbbell are on the fluted_block.
        - Bottle and tissue-box are on the table.
        """
        if (
            self.check_on(self.drill, self.fluted_block) and
            self.check_on(self.dumbbell, self.fluted_block) and
            self.check_on(self.bottle, self.table) and
            self.check_on(self.tissue_box, self.table)
        ):
            return True
        return False
