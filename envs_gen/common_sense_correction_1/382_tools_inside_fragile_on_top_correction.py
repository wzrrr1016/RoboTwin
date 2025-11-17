from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 382_tools_inside_fragile_on_top_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the simulation environment."""
        # Add the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add maintenance tools and other objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.drill = self.add_actor("drill", "drill")
        self.microphone = self.add_actor("microphone", "microphone")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.green_block = self.add_actor("green_block", "green_block")
        
        # Add distractor objects to the environment
        distractor_list = ['pet-collar', 'table-tennis', 'pot-with-plant']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions to complete the task."""
        # Step 1: Place screwdriver into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver into wooden_box:", success)
        if not success:
            return self.info

        # Step 2: Place microphone into wooden_box (wrong action)
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("Place microphone into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing microphone on wooden_box
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("Place microphone on wooden_box (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place drill into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill into wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place tissue-box on wooden_box
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("Place tissue-box on wooden_box:", success)
        if not success:
            return self.info

        # Step 6: Place green_block on wooden_box
        success = self.pick_and_place(self.green_block, self.wooden_box)
        print("Place green_block on wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check if maintenance tools (screwdriver, drill) are inside the wooden_box
        # This is inferred by checking they are NOT on top of the wooden_box
        maintenance_tools_inside = (
            not self.check_on(self.screwdriver, self.wooden_box) and
            not self.check_on(self.drill, self.wooden_box)
        )
        
        # Check if lightweight items are on top of the wooden_box
        lightweight_on_top = (
            self.check_on(self.microphone, self.wooden_box) and
            self.check_on(self.tissue_box, self.wooden_box) and
            self.check_on(self.green_block, self.wooden_box)
        )
        
        return maintenance_tools_inside and lightweight_on_top
