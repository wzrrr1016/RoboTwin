from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 377_store_toys_and_tools_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        """
        # Add the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the main objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.hammer = self.add_actor("hammer", "hammer")
        self.bottle = self.add_actor("bottle", "bottle")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects
        distractor_list = ["pet-collar", "tissue-box", "roll-paper"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot actions to complete the task.
        """
        # 1. Place toycar (toy) into wooden_box
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("Place toycar into wooden_box:", success)
        if not success:
            return self.info

        # 2. Wrong action: Place bottle (liquid) into wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Wrongly place bottle into wooden_box:", success)
        if not success:
            return self.info

        # 3. Recovery: Remove bottle from wooden_box and place on table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle to table:", success)
        if not success:
            return self.info

        # 4. Place hammer (tool) into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Place hammer into wooden_box:", success)
        if not success:
            return self.info

        # 5. Place bread (food) on table
        success = self.pick_and_place(self.bread, self.table)
        print("Place bread on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        Toys and tools should be in the wooden_box, food and liquids should be on the table.
        """
        # Check if toys and tools are in the wooden_box
        toycar_in_box = self.check_on(self.toycar, self.wooden_box)
        hammer_in_box = self.check_on(self.hammer, self.wooden_box)
        
        # Check if food and liquids are on the table
        bottle_on_table = self.check_on(self.bottle, self.table)
        bread_on_table = self.check_on(self.bread, self.table)
        
        # Return True only if all conditions are satisfied
        return toycar_in_box and hammer_in_box and bottle_on_table and bread_on_table
