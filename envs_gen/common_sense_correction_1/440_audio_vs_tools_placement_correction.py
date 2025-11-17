from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 440_audio_vs_tools_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Containers: plate and fluted_block
        - Objects: bell, small-speaker, screwdriver, drill
        - Distractors: apple, book, shoe, tissue-box, red_block
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add task-relevant objects
        self.bell = self.add_actor("bell", "bell")
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractors
        distractor_list = ["apple", "book", "shoe", "tissue-box", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions as per the task instructions.
        Steps:
        1. Place bell on plate
        2. Place screwdriver in fluted_block
        3. Place drill on plate (wrong placement)
        4. Recover drill to fluted_block
        5. Place small-speaker on plate
        """
        # Step 1: Place bell on plate
        success = self.pick_and_place(self.bell, self.plate)
        print("Place bell on plate:", success)
        if not success:
            return self.info

        # Step 2: Place screwdriver in fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver in fluted_block:", success)
        if not success:
            return self.info

        # Step 3: Place drill on plate (wrong placement)
        success = self.pick_and_place(self.drill, self.plate)
        print("Place drill on plate (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover drill to fluted_block
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Recover drill to fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place small-speaker on plate
        success = self.pick_and_place(self.small_speaker, self.plate)
        print("Place small-speaker on plate:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are in their correct final positions:
        - Sound-producing items (bell, small-speaker) on plate
        - Handheld repair tools (screwdriver, drill) in fluted_block
        """
        return (
            self.check_on(self.bell, self.plate) and
            self.check_on(self.small_speaker, self.plate) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.drill, self.fluted_block)
        )
