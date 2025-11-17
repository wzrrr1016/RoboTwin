from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 261_organize_light_toys_and_paper_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the objects
        self.book = self.add_actor("book", "book")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractors
        distractor_list = ["apple", "baguette", "mug", "shoe", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick book and place into fluted_block
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Pick book:", success)
        if not success:
            return self.info

        # Step 2: Pick pink_block and place into fluted_block
        success = self.pick_and_place(self.pink_block, self.fluted_block)
        print("Pick pink_block:", success)
        if not success:
            return self.info

        # Step 3: Pick drill and place into fluted_block (wrong action)
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Pick drill (wrong):", success)
        if not success:
            return self.info

        # Step 4: Pick drill from fluted_block and place on table (recovery)
        success = self.pick_and_place(self.drill, self.table)
        print("Pick drill and place on table:", success)
        if not success:
            return self.info

        # Step 5: Pick green_block and place into fluted_block
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Pick green_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all correct items are in the fluted_block
        book_on = self.check_on(self.book, self.fluted_block)
        pink_on = self.check_on(self.pink_block, self.fluted_block)
        green_on = self.check_on(self.green_block, self.fluted_block)
        
        # Check if the drill is on the table (not in fluted_block)
        drill_on_table = self.check_on(self.drill, self.table)
        
        return book_on and pink_on and green_on and drill_on_table
