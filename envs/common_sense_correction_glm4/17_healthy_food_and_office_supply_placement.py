from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class healthy_food_and_office_supply_placement(Imagine_Task):
    def load_actors(self):
        # Load the actors into the environment
        self.coaster = self.add_actor("coaster", "coaster")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.scanner = self.add_actor("scanner", "scanner")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.stapler = self.add_actor("stapler", "stapler")
        self.french_fries = self.add_actor("french_fries", "french_fries")

    def play_once(self):
        # Pick up the scanner and place it into the coaster
        success = self.pick_and_place(self.scanner, self.coaster)
        print("Pick and place scanner:", success)
        if not success:
            return self.info

        # Attempt to pick up the pot-with-plant and place it into the wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Pick and place pot-with-plant:", success)
        if not success:
            return self.info

        # Since the pot-with-plant was placed incorrectly, pick it up from the wooden_box
        # and place it into the coaster as a recovery action
        success = self.pick_and_place(self.pot_with_plant, self.coaster)
        print("Recover pot-with-plant:", success)
        if not success:
            return self.info

        # Pick up the stapler and place it into the coaster
        success = self.pick_and_place(self.stapler, self.coaster)
        print("Pick and place stapler:", success)
        if not success:
            return self.info

        # Pick up the french_fries and place them into the wooden_box
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("Pick and place french_fries:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all items are in the correct container
        if (self.check_on(self.scanner, self.coaster) and
            self.check_on(self.stapler, self.coaster) and
            self.check_on(self.french_fries, self.wooden_box)):
            return True
        return False

# Example usage:
# task = PlaceItemsTask()
# task.load_actors()
# task.play_once()
# if task.check_success():
#     print("Task completed successfully.")
# else:
#     print("Task failed.")
