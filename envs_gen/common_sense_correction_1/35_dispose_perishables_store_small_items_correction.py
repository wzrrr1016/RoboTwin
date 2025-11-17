from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 35_dispose_perishables_store_small_items_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers, target objects, and distractors.
        """
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add target objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.mouse = self.add_actor("mouse", "mouse")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractors
        distractor_list = [
            "screwdriver", "hammer", "pot-with-plant", "small-speaker", "alarm-clock"
        ]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        This includes both correct and recovery actions as specified in the task.
        """
        # Step 1: Wrong placement of apple into shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Place apple into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - move apple to dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Recover apple to dustbin:", success)
        if not success:
            return self.info

        # Step 3: Place bread into dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Place bread into dustbin:", success)
        if not success:
            return self.info

        # Step 4: Place mouse into shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Place mouse into shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place toycar into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Place toycar into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        This is done by verifying the final positions of all target objects.
        """
        if (
            self.check_on(self.apple, self.dustbin) and
            self.check_on(self.bread, self.dustbin) and
            self.check_on(self.mouse, self.shoe_box) and
            self.check_on(self.toycar, self.shoe_box)
        ):
            return True
        return False
