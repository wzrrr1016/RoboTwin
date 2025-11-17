from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 78_dispose_single_use_correct_heavy_keep_out(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the dustbin (container), the main objects (bottle, shampoo, dumbbell, tissue-box),
        and the distractor objects.
        """
        # Add the dustbin as a container
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add the main objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")

        # Add distractor objects
        distractor_list = ["calculator", "toycar", "book", "shoe", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot first performs a wrong action (placing the bottle in the dustbin),
        then recovers by placing it back on the table. It then correctly places the
        tissue-box in the dustbin and the other items on the table.
        """
        # Wrong action: place bottle into dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Pick bottle into dustbin (wrong):", success)
        if not success:
            return self.info

        # Recovery: place bottle back on the table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle to table:", success)
        if not success:
            return self.info

        # Correct action: place tissue-box into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Put tissue-box into dustbin:", success)
        if not success:
            return self.info

        # Place dumbbell on the table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Put dumbbell on table:", success)
        if not success:
            return self.info

        # Place shampoo on the table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Put shampoo on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the robot has successfully completed the task.
        The success condition is:
        - Tissue-box is in the dustbin
        - Dumbbell and shampoo are on the table
        - Bottle is on the table (after recovery)
        """
        if (
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.dumbbell, self.table) and
            self.check_on(self.shampoo, self.table) and
            self.check_on(self.bottle, self.table)
        ):
            return True
        return False
