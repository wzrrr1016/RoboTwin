from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 322_put_toys_and_blocks_into_shoebox_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (containers and objects) into the simulation environment.
        Adds the shoe_box as a container and the toycar and blocks as objects.
        Adds distractors as specified in the task description.
        """
        # Add the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add the required objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.green_block = self.add_actor("green_block", "green_block")
        
        # Add distractors to the environment
        distractor_list = ['screwdriver', 'mouse', 'jam-jar', 'alarm-clock', 'baguette']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm to complete the task.
        The sequence includes:
        1. Place toycar into shoe_box
        2. Place purple_block on shoe_box (wrong placement)
        3. Recover by placing purple_block into shoe_box
        4. Place orange_block into shoe_box
        5. Place green_block into shoe_box
        """
        # Step 1: Place toycar into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Place toycar:", success)
        if not success:
            return self.info

        # Step 2: Place purple_block on shoe_box (wrong placement)
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("First purple_block placement:", success)
        if not success:
            return self.info

        # Step 3: Recovery - Place purple_block into shoe_box
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("Recovery purple_block placement:", success)
        if not success:
            return self.info

        # Step 4: Place orange_block into shoe_box
        success = self.pick_and_place(self.orange_block, self.shoe_box)
        print("Place orange_block:", success)
        if not success:
            return self.info

        # Step 5: Place green_block into shoe_box
        success = self.pick_and_place(self.green_block, self.shoe_box)
        print("Place green_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if all required objects (toycar and blocks) are on the shoe_box.
        This confirms that the task has been successfully completed.
        """
        return (
            self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.purple_block, self.shoe_box) and
            self.check_on(self.orange_block, self.shoe_box) and
            self.check_on(self.green_block, self.shoe_box)
        )
