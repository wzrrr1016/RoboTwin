from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 424_serve_food_and_tableware_with_tool_correction(Imagine_Task):
    def load_actors(self):
        # Add the plate and relevant objects
        self.plate = self.add_actor("plate", "plate")
        self.bread = self.add_actor("bread", "bread")
        self.mug = self.add_actor("mug", "mug")
        self.knife = self.add_actor("knife", "knife")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors to the environment
        distractor_list = ["pot-with-plant", "toycar", "book", "shoe", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrong action - Place screwdriver on plate
        success = self.pick_and_place(self.screwdriver, self.plate)
        print("Pick and place screwdriver onto plate (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - Place screwdriver on table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Pick and place screwdriver onto table (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place edible and dining items on the plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Pick and place bread onto plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mug, self.plate)
        print("Pick and place mug onto plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.knife, self.plate)
        print("Pick and place knife onto plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if edible and dining items are on the plate
        edible_on_plate = self.check_on(self.bread, self.plate)
        drinkware_on_plate = self.check_on(self.mug, self.plate)
        utensil_on_plate = self.check_on(self.knife, self.plate)

        # Check if repair tool is NOT on the plate
        repair_tool_off_plate = not self.check_on(self.screwdriver, self.plate)

        return edible_on_plate and drinkware_on_plate and utensil_on_plate and repair_tool_off_plate
