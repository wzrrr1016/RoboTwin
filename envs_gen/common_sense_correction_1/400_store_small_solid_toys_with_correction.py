from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 400_store_small_solid_toys_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Create the shoe_box container.
        - Create the small solid toys (purple_block, red_block, yellow_block).
        - Create the small-speaker (a distractor object in this task).
        - Add the specified distractors to the environment.
        """
        # Create the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create the small solid toys
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Create the small-speaker (not a toy in this task)
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractors to the environment
        distractor_list = ['pot-with-plant', 'dumbbell', 'drill', 'book', 'apple']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Pick and place the purple_block into the shoe_box.
        - Pick and place the small-speaker into the shoe_box (wrong action).
        - Pick and place the small-speaker back onto the table (recovery).
        - Pick and place the red_block and yellow_block into the shoe_box.
        """
        # Step 1: Pick purple_block and place into shoe_box
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("Pick purple_block and place into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Pick small-speaker and place into shoe_box (wrong action)
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Pick small-speaker and place into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick small-speaker from shoe_box and place onto table (recovery)
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Pick small-speaker from shoe_box and place onto table (recovery):", success)
        if not success:
            return self.info

        # Step 4: Pick red_block and place into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Pick red_block and place into shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Pick yellow_block and place into shoe_box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Pick yellow_block and place into shoe_box:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All three small solid toys (purple_block, red_block, yellow_block) are in the shoe_box.
        - The small-speaker is on the table (not in the shoe_box).
        """
        # Check if all three blocks are in the shoe_box
        blocks_in_shoe_box = (
            self.check_on(self.purple_block, self.shoe_box) and
            self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.yellow_block, self.shoe_box)
        )
        
        # Check if the small-speaker is on the table (after recovery)
        speaker_on_table = self.check_on(self.small_speaker, self.table)
        
        # Return True if all conditions are met
        return blocks_in_shoe_box and speaker_on_table
