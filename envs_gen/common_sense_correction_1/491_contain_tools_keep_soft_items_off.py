from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 491_contain_tools_keep_soft_items_off(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Distractors are added separately using the add_distractors method.
        """
        # Add the coaster as the container
        self.coaster = self.add_actor("coaster", "coaster")

        # Add the relevant objects
        self.knife = self.add_actor("knife", "knife")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractors to the environment
        distractor_list = ["calculator", "book", "pot-with-plant", "sand-clock", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        Each action is followed by a success check. If any action fails, the task is terminated.
        """
        # 1. Place knife on the coaster
        success = self.pick_and_place(self.knife, self.coaster)
        print("Place knife on coaster:", success)
        if not success:
            return self.info

        # 2. Place screwdriver on the coaster
        success = self.pick_and_place(self.screwdriver, self.coaster)
        print("Place screwdriver on coaster:", success)
        if not success:
            return self.info

        # 3. Wrongly place tissue-box on the coaster
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("Wrongly place tissue-box on coaster:", success)
        if not success:
            return self.info

        # 4. Recovery: Move tissue-box back to the table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Recover tissue-box to table:", success)
        if not success:
            return self.info

        # 5. Place toycar on the table
        success = self.pick_and_place(self.toycar, self.table)
        print("Place toycar on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of the objects.
        The task is considered successful if:
        - Knife and screwdriver are on the coaster
        - Tissue-box and toycar are NOT on the coaster
        """
        # Check if knife and screwdriver are on the coaster
        knife_on_coaster = self.check_on(self.knife, self.coaster)
        screwdriver_on_coaster = self.check_on(self.screwdriver, self.coaster)

        # Check if tissue-box and toycar are NOT on the coaster
        tissue_not_on_coaster = not self.check_on(self.tissue_box, self.coaster)
        toycar_not_on_coaster = not self.check_on(self.toycar, self.coaster)

        # Return True if all conditions are met
        return (
            knife_on_coaster
            and screwdriver_on_coaster
            and tissue_not_on_coaster
            and toycar_not_on_coaster
        )
