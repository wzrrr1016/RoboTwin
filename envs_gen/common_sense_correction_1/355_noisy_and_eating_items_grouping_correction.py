from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 355_noisy_and_eating_items_grouping_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.bell = self.add_actor("bell", "bell")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors
        distractor_list = ['book', 'shoe', 'pot-with-plant', 'markpen', 'toycar']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        """
        # Place noisy items on fluted_block
        success = self.pick_and_place(self.bell, self.fluted_block)
        print("Place bell on fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Place small-speaker on fluted_block:", success)
        if not success:
            return self.info

        # Wrong placement of food item on fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Wrongly place french_fries on fluted_block:", success)
        if not success:
            return self.info

        # Recovery: move food item to tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Move french_fries to tray:", success)
        if not success:
            return self.info

        # Place eating utensils on tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Place fork on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.knife, self.tray)
        print("Place knife on tray:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all relevant objects.
        """
        # Check if noisy items are on fluted_block
        bell_on_fluted = self.check_on(self.bell, self.fluted_block)
        speaker_on_fluted = self.check_on(self.small_speaker, self.fluted_block)

        # Check if eating/serving items are on tray
        fries_on_tray = self.check_on(self.french_fries, self.tray)
        fork_on_tray = self.check_on(self.fork, self.tray)
        knife_on_tray = self.check_on(self.knife, self.tray)

        # Return True only if all conditions are met
        return bell_on_fluted and speaker_on_fluted and fries_on_tray and fork_on_tray and knife_on_tray
