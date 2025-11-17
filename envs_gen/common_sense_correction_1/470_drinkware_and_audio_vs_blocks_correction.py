from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 470_drinkware_and_audio_vs_blocks_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        - Containers: coaster, dustbin
        - Objects: cup_without_handle, small-speaker, yellow_block, blue_block
        - Distractors: calculator, pet-collar, shoe, book, tissue-box
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.cup = self.add_actor("cup_without_handle", "cup_without_handle")
        self.speaker = self.add_actor("small-speaker", "small-speaker")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "shoe", "book", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm:
        1. Pick cup_without_handle and place it on the coaster.
        2. Pick small-speaker and place it on the coaster.
        3. Pick yellow_block and place it on the coaster (wrong placement).
        4. Pick yellow_block from the coaster and place it into the dustbin (recovery).
        5. Pick blue_block and place it into the dustbin.
        """
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.speaker, self.coaster)
        print("Place speaker on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.yellow_block, self.coaster)
        print("Place yellow_block on coaster (wrong):", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.yellow_block, self.dustbin)
        print("Recover yellow_block to dustbin:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.dustbin)
        print("Place blue_block in dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - cup_without_handle and small-speaker are on the coaster.
        - yellow_block and blue_block are in the dustbin.
        """
        return (
            self.check_on(self.cup, self.coaster) and
            self.check_on(self.speaker, self.coaster) and
            self.check_on(self.yellow_block, self.dustbin) and
            self.check_on(self.blue_block, self.dustbin)
        )
