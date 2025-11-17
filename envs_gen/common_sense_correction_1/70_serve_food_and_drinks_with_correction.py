from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 70_serve_food_and_drinks_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: plate
        - Objects: hamburg, bottle, hammer, teanet
        - Distractors: pot-with-plant, small-speaker, tissue-box, pet-collar
        """
        # Add the plate as the main container
        self.plate = self.add_actor("plate", "plate")
        
        # Add edible and drink-related objects
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add non-food tools and utensils
        self.hammer = self.add_actor("hammer", "hammer")
        self.teanet = self.add_actor("teanet", "teanet")
        
        # Add distractor objects to the environment
        distractor_list = ["pot-with-plant", "small-speaker", "tissue-box", "pet-collar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's sequence of actions:
        1. Place hammer on plate (wrong action)
        2. Recover by placing hammer on table
        3. Place hamburg on plate
        4. Place bottle on plate
        5. Place teanet on table
        """
        # Wrong action: place hammer on plate
        success = self.pick_and_place(self.hammer, self.plate)
        print("Pick hammer and place on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: move hammer to table
        success = self.pick_and_place(self.hammer, self.table)
        print("Pick hammer from plate and place on table (recovery):", success)
        if not success:
            return self.info

        # Place edible item (hamburg) on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Pick hamburg and place on plate:", success)
        if not success:
            return self.info

        # Place drink-related item (bottle) on plate
        success = self.pick_and_place(self.bottle, self.plate)
        print("Pick bottle and place on plate:", success)
        if not success:
            return self.info

        # Place non-food utensil (teanet) on table
        success = self.pick_and_place(self.teanet, self.table)
        print("Pick teanet and place on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - hamburg and bottle are on the plate
        - hammer and teanet are not on the plate
        """
        # Check if edible and drink-related items are on the plate
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)
        bottle_on_plate = self.check_on(self.bottle, self.plate)
        
        # Check if non-food items are not on the plate
        hammer_not_on_plate = not self.check_on(self.hammer, self.plate)
        teanet_not_on_plate = not self.check_on(self.teanet, self.plate)
        
        # Return True only if all conditions are satisfied
        return hamburg_on_plate and bottle_on_plate and hammer_not_on_plate and teanet_not_on_plate
