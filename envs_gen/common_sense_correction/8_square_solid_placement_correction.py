from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 8_square_solid_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add main objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")

        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'table-tennis', 'roll-paper', 'alarm-clock']
        self.add_distractors(distractor_list)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions the robot arm should perform.
        """
        # Step 1: Pick red_block and place it into tray (wrong action)
        success = self.pick_and_place(self.red_block, self.tray)
        print("Pick red_block and place into tray (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - Pick red_block from tray and place it into wooden_box
        success = self.pick_and_place(self.red_block, self.wooden_box)
        print("Pick red_block from tray and place into wooden_box (recovery):", success)
        if not success:
            return self.info

        # Step 3: Pick purple_block and place it into wooden_box
        success = self.pick_and_place(self.purple_block, self.wooden_box)
        print("Pick purple_block and place into wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Pick orange_block and place it into wooden_box
        success = self.pick_and_place(self.orange_block, self.wooden_box)
        print("Pick orange_block and place into wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Pick shampoo and place it into tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick shampoo and place into tray:", success)
        if not success:
            return self.info

        # Step 6: Pick small_speaker and place it into tray
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Pick small_speaker and place into tray:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        """
        # Check if all square solid objects are in the wooden_box
        blocks_in_wooden_box = (
            self.check_on(self.red_block, self.wooden_box) and
            self.check_on(self.purple_block, self.wooden_box) and
            self.check_on(self.orange_block, self.wooden_box)
        )

        # Check if shampoo and small_speaker are in the tray
        others_in_tray = (
            self.check_on(self.shampoo, self.tray) and
            self.check_on(self.small_speaker, self.tray)
        )

        # Return True only if all conditions are met
        return blocks_in_wooden_box and others_in_tray
