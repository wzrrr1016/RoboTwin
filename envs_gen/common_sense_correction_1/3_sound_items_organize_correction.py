from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 3_sound_items_organize_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the simulation environment."""
        # Create the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create the main objects
        self.bell = self.add_actor("bell", "bell")
        self.microphone = self.add_actor("microphone", "microphone")
        self.book = self.add_actor("book", "book")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        
        # Add distractor objects to the environment
        distractor_list = ["apple", "hammer", "shoe", "baguette", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions for the task."""
        # 1. Place bell in fluted_block
        success = self.pick_and_place(self.bell, self.fluted_block)
        print("Place bell:", success)
        if not success:
            return self.info

        # 2. Place microphone in fluted_block
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("Place microphone:", success)
        if not success:
            return self.info

        # 3. Wrong action: Place book in fluted_block
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Wrongly place book:", success)
        if not success:
            return self.info

        # 4. Recovery: Place book back on table
        success = self.pick_and_place(self.book, self.table)
        print("Recover book:", success)
        if not success:
            return self.info

        # 5. Place sand-clock on table
        success = self.pick_and_place(self.sand_clock, self.table)
        print("Place sand-clock:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check if sound-producing/capturing items are in fluted_block
        bell_in_container = self.check_on(self.bell, self.fluted_block)
        mic_in_container = self.check_on(self.microphone, self.fluted_block)
        
        # Check if visual/reading items are on the table
        book_on_table = self.check_on(self.book, self.table)
        sand_clock_on_table = self.check_on(self.sand_clock, self.table)
        
        # Return True only if all conditions are met
        return (bell_in_container and mic_in_container and 
                book_on_table and sand_clock_on_table)
