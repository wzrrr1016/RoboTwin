from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 380_place_food_and_utensils_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes the plate, edible items, eating utensils, and distractors.
        """
        # Add the main container
        self.plate = self.add_actor("plate", "plate")
        
        # Add edible item and eating utensil
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        
        # Add non-edible distractor object
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        
        # Add distractor objects to the environment
        distractor_list = ['pet-collar', 'toycar', 'tissue-box', 'book', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation.
        Includes a wrong action and recovery followed by correct actions.
        """
        # Wrong action: Place small speaker on plate
        success = self.pick_and_place(self.small_speaker, self.plate)
        print("Pick small-speaker and place on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: Move small speaker back to table
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Pick small-speaker and place on table (recovery):", success)
        if not success:
            return self.info

        # Correct action: Place fork on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Pick fork and place on plate:", success)
        if not success:
            return self.info

        # Correct action: Place french fries on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Pick french_fries and place on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        Checks if edible items and utensils are on the plate,
        and the distractor is not on the plate.
        """
        # Check if fork (eating utensil) is on the plate
        fork_on_plate = self.check_on(self.fork, self.plate)
        
        # Check if french fries (edible item) is on the plate
        french_fries_on_plate = self.check_on(self.french_fries, self.plate)
        
        # Check if small speaker (distractor) is NOT on the plate
        speaker_not_on_plate = not self.check_on(self.small_speaker, self.plate)
        
        # Return True only if all conditions are met
        return fork_on_plate and french_fries_on_plate and speaker_not_on_plate
