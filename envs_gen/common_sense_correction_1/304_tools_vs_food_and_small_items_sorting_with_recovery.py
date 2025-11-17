from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 304_tools_vs_food_and_small_items_sorting_with_recovery(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        Adds containers, task-relevant objects, and distractors.
        """
        # Add containers to the environment
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add task-relevant objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.apple = self.add_actor("apple", "apple")
        self.cup = self.add_actor("cup", "cup")
        self.markpen = self.add_actor("markpen", "markpen")
        
        # Add distractor objects to the environment
        distractor_list = ['pet-collar', 'dumbbell', 'small-speaker', 'battery', 'microphone']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot arm actions to complete the task.
        Includes error recovery for incorrect placements.
        """
        # 1. Place hammer on fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Hammer placed on fluted_block:", success)
        if not success:
            return self.info

        # 2. Wrongly place apple on fluted_block (incorrect action)
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Apple wrong placement on fluted_block:", success)
        if not success:
            return self.info

        # 3. Recovery: Move apple from fluted_block to tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Apple recovery to tray:", success)
        if not success:
            return self.info

        # 4. Place screwdriver on fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Screwdriver placed on fluted_block:", success)
        if not success:
            return self.info

        # 5. Place cup on tray
        success = self.pick_and_place(self.cup, self.tray)
        print("Cup placed on tray:", success)
        if not success:
            return self.info

        # 6. Place markpen on tray
        success = self.pick_and_place(self.markpen, self.tray)
        print("Markpen placed on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if all task requirements are successfully completed.
        Checks if hand tools are on fluted_block and edible/stationery items are on tray.
        """
        # Check hand tools on fluted_block
        hammer_on_fluted = self.check_on(self.hammer, self.fluted_block)
        screwdriver_on_fluted = self.check_on(self.screwdriver, self.fluted_block)
        
        # Check edible/drinkable and stationery items on tray
        apple_on_tray = self.check_on(self.apple, self.tray)
        cup_on_tray = self.check_on(self.cup, self.tray)
        markpen_on_tray = self.check_on(self.markpen, self.tray)
        
        # Return True only if all conditions are satisfied
        return (hammer_on_fluted and screwdriver_on_fluted and 
                apple_on_tray and cup_on_tray and markpen_on_tray)
