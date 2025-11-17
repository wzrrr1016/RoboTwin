from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 396_store_play_and_reading_items_with_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Create container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create main objects
        self.book = self.add_actor("book", "book")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.hammer = self.add_actor("hammer", "hammer")
        self.apple = self.add_actor("apple", "apple")
        
        # Add distractors
        distractor_list = ["alarm-clock", "small-speaker", "tissue-box", "microphone", "calculator"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Place lightweight reading/play items in shoe box
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Place book:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.pink_block, self.shoe_box)
        print("Place pink_block:", success)
        if not success:
            return self.info
            
        # Wrong action - place heavy tool in box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Place hammer (wrong):", success)
        if not success:
            return self.info
            
        # Recovery - remove heavy tool from box
        success = self.pick_and_place(self.hammer, self.table)
        print("Remove hammer:", success)
        if not success:
            return self.info
            
        # Place another lightweight item in box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Place red_block:", success)
        if not success:
            return self.info
            
        # Place perishable food on table
        success = self.pick_and_place(self.apple, self.table)
        print("Place apple:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check lightweight items in shoe box
        book_in_box = self.check_on(self.book, self.shoe_box)
        pink_in_box = self.check_on(self.pink_block, self.shoe_box)
        red_in_box = self.check_on(self.red_block, self.shoe_box)
        
        # Check heavy tool and perishable on table
        hammer_on_table = self.check_on(self.hammer, self.table)
        apple_on_table = self.check_on(self.apple, self.table)
        
        # All conditions must be satisfied
        return (book_in_box and pink_in_box and red_in_box and 
                hammer_on_table and apple_on_table)
