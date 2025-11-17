from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 405_organize_liquids_and_drinkware_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the target objects
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.markpen = self.add_actor("markpen", "markpen")

        # Add distractors as specified in the scene
        distractor_list = ['shoe', 'dumbbell', 'pot-with-plant', 'toycar', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot actions to complete the task.
        """
        # Step 1: Place shampoo into fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Pick shampoo and place into fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place markpen into fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Wrongly place markpen into fluted_block:", success)
        if not success:
            return self.info

        # Step 3: Recovery - Place markpen on the table
        success = self.pick_and_place(self.markpen, self.table)
        print("Recover markpen to table:", success)
        if not success:
            return self.info

        # Step 4: Place bottle into fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Pick bottle and place into fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place cup_without_handle into fluted_block
        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("Pick cup_without_handle and place into fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        """
        # Check if shampoo, bottle, and cup_without_handle are in the fluted_block
        # and markpen is not in the fluted_block
        if (self.check_on(self.shampoo, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.cup_without_handle, self.fluted_block) and
            not self.check_on(self.markpen, self.fluted_block)):
            return True
        return False
