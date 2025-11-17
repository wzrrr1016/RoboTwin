from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 222_dispose_metal_keep_decor_correction(Imagine_Task):
    def load_actors(self):
        # Add the dustbin as a container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add the target objects
        self.knife = self.add_actor("knife", "knife")
        self.stapler = self.add_actor("stapler", "stapler")
        self.toycar = self.add_actor("toycar", "toycar")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        # Add distractors
        distractor_list = ["book", "apple", "tissue-box", "mug", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick knife and place into dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Pick and place knife:", success)
        if not success:
            return self.info

        # Step 2: Pick stapler and place into dustbin
        success = self.pick_and_place(self.stapler, self.dustbin)
        print("Pick and place stapler:", success)
        if not success:
            return self.info

        # Step 3: Wrong action - Pick toycar and place into dustbin
        success = self.pick_and_place(self.toycar, self.dustbin)
        print("Pick and place toycar (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery - Pick toycar from dustbin and place on table
        success = self.pick_and_place(self.toycar, self.table)
        print("Recover toycar to table:", success)
        if not success:
            return self.info

        # Step 5: Pick pot-with-plant and place on table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Pick and place pot-with-plant:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if knife and stapler are in the dustbin
        # Check if toycar and pot-with-plant are on the table
        if (
            self.check_on(self.knife, self.dustbin) and
            self.check_on(self.stapler, self.dustbin) and
            self.check_on(self.toycar, self.table) and
            self.check_on(self.pot_with_plant, self.table)
        ):
            return True
        return False
