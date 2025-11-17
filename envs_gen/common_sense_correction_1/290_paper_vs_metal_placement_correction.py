from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 290_paper_vs_metal_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: plate and dustbin
        - Objects: tissue-box, fork, bell
        - Distractors: calculator, table-tennis, pot-with-plant, red_block, shoe
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.fork = self.add_actor("fork", "fork")
        self.bell = self.add_actor("bell", "bell")

        # Add distractors
        distractor_list = ["calculator", "table-tennis", "pot-with-plant", "red_block", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions to complete the task:
        1. Pick bell and place it into dustbin (wrong action)
        2. Pick bell from dustbin and place it onto plate (recovery)
        3. Pick tissue-box and place it into dustbin
        4. Pick fork and place it onto plate
        """
        # Step 1: Pick bell and place into dustbin (wrong action)
        success = self.pick_and_place(self.bell, self.dustbin)
        print("Pick bell to dustbin:", success)
        if not success:
            return self.info

        # Step 2: Pick bell from dustbin and place onto plate (recovery)
        success = self.pick_and_place(self.bell, self.plate)
        print("Pick bell to plate:", success)
        if not success:
            return self.info

        # Step 3: Pick tissue-box and place into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Pick tissue-box to dustbin:", success)
        if not success:
            return self.info

        # Step 4: Pick fork and place onto plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Pick fork to plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying:
        - Tissue-box is in the dustbin
        - Fork is on the plate
        - Bell is on the plate (after recovery from dustbin)
        """
        if (
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.fork, self.plate) and
            self.check_on(self.bell, self.plate)
        ):
            return True
        return False
