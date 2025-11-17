from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 2_liquid_container_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: shoe_box and fluted_block
        - Objects: can, bottle, mug, cup
        - Distractors: calculator, knife, hammer, toycar, book, red_block
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.can = self.add_actor("can", "can")
        self.bottle = self.add_actor("bottle", "bottle")
        self.mug = self.add_actor("mug", "mug")
        self.cup = self.add_actor("cup", "cup")

        # Add distractors
        distractors = ["calculator", "knife", "hammer", "toycar", "book", "red_block"]
        self.add_distractors(distractors)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Place can and bottle into shoe_box (liquid containers)
        - Place mug into fluted_block (wrong action), then recover by placing it into shoe_box
        - Place cup into shoe_box (liquid container)
        """
        # Step 1: Pick can and place into shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        if not success:
            return self.info

        # Step 2: Pick bottle and place into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        if not success:
            return self.info

        # Step 3: Pick mug and place into fluted_block (wrong action)
        success = self.pick_and_place(self.mug, self.fluted_block)
        if not success:
            return self.info

        # Step 4: Pick mug from fluted_block and place into shoe_box (recovery)
        success = self.pick_and_place(self.mug, self.shoe_box)
        if not success:
            return self.info

        # Step 5: Pick cup and place into shoe_box
        success = self.pick_and_place(self.cup, self.shoe_box)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All liquid containers (can, bottle, mug, cup) must be in the shoe_box
        - No objects should be in the fluted_block
        """
        # Check if all liquid containers are in the shoe_box
        if (
            self.check_on(self.can, self.shoe_box) and
            self.check_on(self.bottle, self.shoe_box) and
            self.check_on(self.mug, self.shoe_box) and
            self.check_on(self.cup, self.shoe_box)
        ):
            return True
        return False
