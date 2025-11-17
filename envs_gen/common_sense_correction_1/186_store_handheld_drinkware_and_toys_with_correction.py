from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 186_store_handheld_drinkware_and_toys_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the container (shoe_box), relevant objects (mug, cup_with_handle, red_block, knife),
        and distractor objects.
        """
        # Add the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add relevant objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.red_block = self.add_actor("red_block", "red_block")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractor objects
        distractor_list = ['book', 'alarm-clock', 'calculator', 'battery', 'tissue-box']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The task includes:
        1. Pick mug and place it into shoe_box
        2. Pick knife and place it into shoe_box (wrong action)
        3. Pick knife from shoe_box and place it on table (recovery)
        4. Pick cup_with_handle and place it into shoe_box
        5. Pick red_block and place it into shoe_box
        """
        # Step 1: Pick mug and place into shoe_box
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Pick mug:", success)
        if not success:
            return self.info

        # Step 2: Wrong action - Pick knife and place into shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Pick knife (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recovery - Pick knife from shoe_box and place on table
        success = self.pick_and_place(self.knife, self.table)
        print("Recover knife:", success)
        if not success:
            return self.info

        # Step 4: Pick cup_with_handle and place into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Pick cup_with_handle:", success)
        if not success:
            return self.info

        # Step 5: Pick red_block and place into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Pick red_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The task is considered successful if:
        - Mug is in the shoe_box
        - Cup_with_handle is in the shoe_box
        - Red_block is in the shoe_box
        - Knife is NOT in the shoe_box (i.e., it was successfully recovered)
        """
        # Check if all correct objects are in the shoe_box
        mug_on = self.check_on(self.mug, self.shoe_box)
        cup_on = self.check_on(self.cup_with_handle, self.shoe_box)
        red_on = self.check_on(self.red_block, self.shoe_box)
        
        # Check if knife is not in the shoe_box
        knife_not_in = not self.check_on(self.knife, self.shoe_box)
        
        return mug_on and cup_on and red_on and knife_not_in
