from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 283_organize_play_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the required objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'book', 'shoe', 'microphone']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place red_block into fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Place green_block into fluted_block
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block:", success)
        if not success:
            return self.info

        # Wrong action: place fork into fluted_block
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Wrong place fork:", success)
        if not success:
            return self.info

        # Recovery: place fork on the table
        success = self.pick_and_place(self.fork, self.table)
        print("Recover fork:", success)
        if not success:
            return self.info

        # Place blue_block into fluted_block
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # Place french_fries on the table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Place french_fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all blocks are in the fluted_block
        blocks_in_container = (
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block)
        )

        # Check if fork and french_fries are on the table
        items_on_table = (
            self.check_on(self.fork, self.table) and
            self.check_on(self.french_fries, self.table)
        )

        return blocks_in_container and items_on_table
