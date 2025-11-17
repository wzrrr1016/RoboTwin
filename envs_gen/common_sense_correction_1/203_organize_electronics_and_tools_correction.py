from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 203_organize_electronics_and_tools_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Add containers: wooden_box and fluted_block
        - Add objects: screwdriver, alarm-clock, mug, microphone, small-speaker
        - Add distractors: shoe, book, pot-with-plant, baguette, toycar
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.mug = self.add_actor("mug", "mug")
        self.microphone = self.add_actor("microphone", "microphone")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractors
        distractor_list = ["shoe", "book", "pot-with-plant", "baguette", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions as specified in the task.
        The sequence includes a correction step for the small-speaker.
        """
        # Step 1: Place microphone in wooden_box
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("Place microphone:", success)
        if not success:
            return self.info

        # Step 2: Place mug on fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug:", success)
        if not success:
            return self.info

        # Step 3: Place small-speaker on fluted_block (wrong placement)
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Place small-speaker (wrong):", success)
        if not success:
            return self.info

        # Step 4: Correct small-speaker placement to wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Recover small-speaker:", success)
        if not success:
            return self.info

        # Step 5: Place alarm-clock in wooden_box
        success = self.pick_and_place(self.alarm_clock, self.wooden_box)
        print("Place alarm-clock:", success)
        if not success:
            return self.info

        # Step 6: Place screwdriver on fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are placed in their correct containers:
        - Small electronic devices (microphone, small-speaker, alarm-clock) in wooden_box
        - Drinkware (mug) and hand tools (screwdriver) on fluted_block
        """
        return (
            self.check_on(self.microphone, self.wooden_box) and
            self.check_on(self.small_speaker, self.wooden_box) and
            self.check_on(self.alarm_clock, self.wooden_box) and
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block)
        )
