from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 428_store_vs_dispose_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the environment.
        Containers (wooden_box and dustbin) are added as actors.
        Required objects (mug, cup_without_handle, small-speaker, red_block, yellow_block) are added as actors.
        Distractors are added using add_distractors.
        """
        # Add containers to the environment
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add required objects to the environment
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.red_block = self.add_actor("red_block", "red_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add distractors to the environment
        distractor_list = ["apple", "book", "shoe", "tissue-box", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Place mug in wooden_box
        2. Place small-speaker in dustbin (wrong action)
        3. Recover small-speaker and place in wooden_box
        4. Place cup_without_handle in wooden_box
        5. Place red_block in dustbin
        6. Place yellow_block in dustbin
        """
        # Step 1: Place mug in wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Place mug:", success)
        if not success:
            return self.info

        # Step 2: Place small-speaker in dustbin (wrong action)
        success = self.pick_and_place(self.small_speaker, self.dustbin)
        print("Wrong place small-speaker:", success)
        if not success:
            return self.info

        # Step 3: Recover small-speaker and place in wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Recover small-speaker:", success)
        if not success:
            return self.info

        # Step 4: Place cup_without_handle in wooden_box
        success = self.pick_and_place(self.cup_without_handle, self.wooden_box)
        print("Place cup_without_handle:", success)
        if not success:
            return self.info

        # Step 5: Place red_block in dustbin
        success = self.pick_and_place(self.red_block, self.dustbin)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Step 6: Place yellow_block in dustbin
        success = self.pick_and_place(self.yellow_block, self.dustbin)
        print("Place yellow_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are placed in the correct containers:
        - Liquid containers and electronics in wooden_box
        - Solid toy blocks in dustbin
        """
        if (self.check_on(self.mug, self.wooden_box) and
            self.check_on(self.cup_without_handle, self.wooden_box) and
            self.check_on(self.small_speaker, self.wooden_box) and
            self.check_on(self.red_block, self.dustbin) and
            self.check_on(self.yellow_block, self.dustbin)):
            return True
        return False
