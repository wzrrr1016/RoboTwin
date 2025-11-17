from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 339_dispose_heavy_electronics_correction(Imagine_Task):
    def load_actors(self):
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects
        self.drill = self.add_actor("drill", "drill")
        self.microphone = self.add_actor("microphone", "microphone")
        self.book = self.add_actor("book", "book")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        
        # Add distractor objects
        distractor_list = ['apple', 'baguette', 'jam-jar', 'tissue-box', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Pick and place drill into dustbin
        success = self.pick_and_place(self.drill, self.dustbin)
        print("Pick drill:", success)
        if not success:
            return self.info

        # Pick and place microphone into dustbin
        success = self.pick_and_place(self.microphone, self.dustbin)
        print("Pick microphone:", success)
        if not success:
            return self.info

        # Mistakenly place book into dustbin
        success = self.pick_and_place(self.book, self.dustbin)
        print("Pick book (wrong):", success)
        if not success:
            return self.info

        # Recovery: place book back on table
        success = self.pick_and_place(self.book, self.table)
        print("Recover book:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if heavy tools and electronics are in dustbin
        drill_in_dustbin = self.check_on(self.drill, self.dustbin)
        mic_in_dustbin = self.check_on(self.microphone, self.dustbin)
        
        # Check if book is on table (not in dustbin)
        book_on_table = self.check_on(self.book, self.table)
        
        # Check if blocks are not in dustbin
        purple_not_in_dustbin = not self.check_on(self.purple_block, self.dustbin)
        pink_not_in_dustbin = not self.check_on(self.pink_block, self.dustbin)
        
        # Return success if all conditions are met
        return (drill_in_dustbin and mic_in_dustbin and 
                book_on_table and purple_not_in_dustbin and pink_not_in_dustbin)
