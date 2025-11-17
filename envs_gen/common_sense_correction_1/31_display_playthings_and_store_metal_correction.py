from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 31_display_playthings_and_store_metal_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Containers: wooden_box, fluted_block
        - Objects: dumbbell, bell, toycar, red_block, blue_block
        - Distractors: book, pot-with-plant, shoe, apple
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.bell = self.add_actor("bell", "bell")
        self.toycar = self.add_actor("toycar", "toycar")
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")

        # Add distractors
        distractor_list = ["book", "pot-with-plant", "shoe", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Actions:
        1. Place red_block on fluted_block
        2. Place toycar on fluted_block
        3. Place bell on fluted_block (wrong action)
        4. Recover bell by placing it into wooden_box
        5. Place blue_block on fluted_block
        6. Place dumbbell into wooden_box
        """
        # 1. Place red_block on fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info

        # 2. Place toycar on fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

        # 3. Place bell on fluted_block (wrong action)
        success = self.pick_and_place(self.bell, self.fluted_block)
        print("Place bell (wrong):", success)
        if not success:
            return self.info

        # 4. Recover bell by placing it into wooden_box
        success = self.pick_and_place(self.bell, self.wooden_box)
        print("Recover bell:", success)
        if not success:
            return self.info

        # 5. Place blue_block on fluted_block
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # 6. Place dumbbell into wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Place dumbbell:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - red_block and blue_block should be on fluted_block
        - toycar should be on fluted_block
        - bell and dumbbell should be in wooden_box
        """
        if (
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.bell, self.wooden_box) and
            self.check_on(self.dumbbell, self.wooden_box)
        ):
            return True
        return False
