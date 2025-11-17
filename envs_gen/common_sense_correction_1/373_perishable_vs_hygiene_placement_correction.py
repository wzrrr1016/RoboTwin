from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 373_perishable_vs_hygiene_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - fluted_block is the container.
        - apple and bread are perishable food items.
        - cup is a disposable/drinkware item.
        - tissue-box is a disposable item (initially placed incorrectly).
        - Distractors are added to the environment.
        """
        # Add the fluted_block as the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the main objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.cup = self.add_actor("cup", "cup")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "screwdriver", "toycar", "alarm-clock", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Place apple into fluted_block.
        2. Place tissue-box into fluted_block (wrong action).
        3. Recover by placing tissue-box on top of fluted_block.
        4. Place bread into fluted_block.
        5. Place cup on top of fluted_block.
        """
        # Step 1: Place apple into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick apple and place into fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Place tissue-box into fluted_block (wrong action)
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Pick tissue-box and place into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing tissue-box on top of fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Recover: Pick tissue-box and place on fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Place bread into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Pick bread and place into fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place cup on top of fluted_block
        success = self.pick_and_place(self.cup, self.fluted_block)
        print("Pick cup and place on fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Perishable items (apple, bread) are in the fluted_block.
        - Disposable/drinkware items (tissue-box, cup) are on top of the fluted_block.
        """
        # Check if apple and bread are in the fluted_block (inside)
        # Note: Since the API only provides `check_on`, we assume that placing into the container
        # results in the object being "on" the container (inside), which is a limitation of the API.
        # In a real-world scenario, a `check_inside` function would be more appropriate.
        apple_in = self.check_on(self.apple, self.fluted_block)
        bread_in = self.check_on(self.bread, self.fluted_block)

        # Check if tissue-box and cup are on top of the fluted_block
        tissue_on = self.check_on(self.tissue_box, self.fluted_block)
        cup_on = self.check_on(self.cup, self.fluted_block)

        # Return True if all conditions are met
        return apple_in and bread_in and tissue_on and cup_on
