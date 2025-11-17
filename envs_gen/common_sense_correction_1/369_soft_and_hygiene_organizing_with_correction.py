from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 369_soft_and_hygiene_organizing_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the container and the relevant objects to be placed.
        Distractors are also added to simulate a realistic environment.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the objects that need to be placed
        self.bread = self.add_actor("bread", "bread")
        self.toycar = self.add_actor("toycar", "toycar")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.shampoo = self.add_actor("shampoo", "shampoo")

        # Add distractors to the environment
        distractor_list = ['calculator', 'screwdriver', 'hammer', 'pot-with-plant', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in one trial.
        This includes placing correct items, making a mistake, and correcting it.
        """
        # Step 1: Place bread into the fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread:", success)
        if not success:
            return self.info

        # Step 2: Place toycar into the fluted_block (wrong action)
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover toycar by placing it back on the table
        success = self.pick_and_place(self.toycar, self.table)
        print("Recover toycar:", success)
        if not success:
            return self.info

        # Step 4: Place tissue-box into the fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box:", success)
        if not success:
            return self.info

        # Step 5: Place shampoo into the fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Place shampoo:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The success condition is that the correct items are in the fluted_block.
        """
        return (
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.tissue_box, self.fluted_block) and
            self.check_on(self.shampoo, self.fluted_block)
        )
