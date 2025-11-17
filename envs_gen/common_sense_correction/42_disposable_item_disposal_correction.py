from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 42_disposable_item_disposal_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the dustbin, disposable items, and distractors.
        """
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add disposable items
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.purple_block = self.add_actor("purple_block", "purple_block")

        # Add distractors to the environment
        distractors = ["calculator", "pet-collar", "table-tennis", "battery", "knife", "screwdriver"]
        self.add_distractors(distractors)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        This includes placing correct items in the dustbin, making a mistake,
        and correcting it by returning the incorrect item to the table.
        """
        # Step 1: Place shampoo into the dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Shampoo placed into dustbin:", success)
        if not success:
            return self.info

        # Step 2: Place french fries into the dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("French fries placed into dustbin:", success)
        if not success:
            return self.info

        # Step 3: Wrong action - Place cup_without_handle into the dustbin
        success = self.pick_and_place(self.cup_without_handle, self.dustbin)
        print("Cup placed into dustbin (wrong action):", success)
        if not success:
            return self.info

        # Step 4: Recovery - Pick cup_without_handle from dustbin and place it back on the table
        success = self.pick_and_place(self.cup_without_handle, self.table)
        print("Cup recovered to table:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The shampoo and french fries must be in the dustbin,
        and the cup_without_handle must be back on the table.
        """
        shampoo_in_dustbin = self.check_on(self.shampoo, self.dustbin)
        french_fries_in_dustbin = self.check_on(self.french_fries, self.dustbin)
        cup_on_table = self.check_on(self.cup_without_handle, self.table)

        return shampoo_in_dustbin and french_fries_in_dustbin and cup_on_table
