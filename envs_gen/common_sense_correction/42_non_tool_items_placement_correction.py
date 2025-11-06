from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 42_non_tool_items_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the plate (container)
        self.plate = self.add_actor("plate", "plate")
        # Load non-tool items
        self.book = self.add_actor("book", "book")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        # Load the tool (drill)
        self.drill = self.add_actor("drill", "drill")

    def play_once(self):
        # Step 1: Pick book and place into plate
        success = self.pick_and_place(self.book, self.plate)
        print("pick place book:", success)
        if not success:
            return self.info

        # Step 2: Pick tissue-box and place into plate
        success = self.pick_and_place(self.tissue_box, self.plate)
        print("pick place tissue-box:", success)
        if not success:
            return self.info

        # Step 3: Pick drill and place into plate (wrong action)
        success = self.pick_and_place(self.drill, self.plate)
        print("pick place drill:", success)
        if not success:
            return self.info

        # Step 4: Recovery: Pick drill from plate and place on table
        success = self.pick_and_place(self.drill, self.table)
        print("pick place drill on table:", success)
        if not success:
            return self.info

        # Step 5: Pick blue_block and place into plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Step 6: Pick green_block and place into plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("pick place green_block:", success)
        if not success:
            return self.info

        # Step 7: Pick red_block and place into plate
        success = self.pick_and_place(self.red_block, self.plate)
        print("pick place red_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check that all non-tool items are on the plate
        non_tool_items = [self.book, self.tissue_box, self.blue_block, self.green_block, self.red_block]
        for item in non_tool_items:
            if not self.check_on(item, self.plate):
                return False

        # Ensure the drill is not on the plate
        if self.check_on(self.drill, self.plate):
            return False

        return True
