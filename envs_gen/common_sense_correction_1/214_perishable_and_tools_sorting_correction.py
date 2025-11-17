from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 214_perishable_and_tools_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: plate and coaster
        - Objects: bread, stapler, hammer
        - Distractors: book, shoe, pot-with-plant, alarm-clock, toycar
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.stapler = self.add_actor("stapler", "stapler")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractors
        distractor_list = ["book", "shoe", "pot-with-plant", "alarm-clock", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Place hammer on coaster
        2. Place bread on coaster (wrong action)
        3. Recover by placing bread on plate
        4. Place stapler on coaster
        """
        # Step 1: Place hammer on coaster
        success = self.pick_and_place(self.hammer, self.coaster)
        print("Place hammer on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place bread on coaster (wrong action)
        success = self.pick_and_place(self.bread, self.coaster)
        print("Place bread on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Recover bread to plate:", success)
        if not success:
            return self.info

        # Step 4: Place stapler on coaster
        success = self.pick_and_place(self.stapler, self.coaster)
        print("Place stapler on coaster:", success)
        if not success:
            return self.info

        return self.info  # Return final status after all actions

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Bread is on the plate
        - Hammer and stapler are on the coaster
        """
        # Check if all required conditions are met
        return (
            self.check_on(self.bread, self.plate) and
            self.check_on(self.hammer, self.coaster) and
            self.check_on(self.stapler, self.coaster)
        )
