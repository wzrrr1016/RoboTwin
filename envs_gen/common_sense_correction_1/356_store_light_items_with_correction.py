from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 356_store_light_items_with_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required objects and distractors in the environment."""
        # Create the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Create objects to be manipulated
        self.book = self.add_actor("book", "book")
        self.markpen = self.add_actor("markpen", "markpen")
        self.bread = self.add_actor("bread", "bread")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractor objects to the environment
        distractor_list = ["dumbbell", "pot-with-plant", "cup-with-liquid"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions for the task."""
        # 1. Place book into wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Place book:", success)
        if not success:
            return self.info

        # 2. Place markpen into wooden_box
        success = self.pick_and_place(self.markpen, self.wooden_box)
        print("Place markpen:", success)
        if not success:
            return self.info

        # 3. Wrongly place bread into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread (wrong):", success)
        if not success:
            return self.info

        # 4. Recovery: Place bread on wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Recover bread:", success)
        if not success:
            return self.info

        # 5. Place hammer on wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Place hammer:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Task success condition: book and markpen are in the wooden_box
        return self.check_on(self.book, self.wooden_box) and self.check_on(self.markpen, self.wooden_box)
