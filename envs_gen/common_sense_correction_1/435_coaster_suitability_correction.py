from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 435_coaster_suitability_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the coaster as a container.
        - Add the objects: can, tissue-box, bread, and pot-with-plant.
        - Add distractor objects as specified in the task description.
        """
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")

        # Add the main objects
        self.can = self.add_actor("can", "can")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bread = self.add_actor("bread", "bread")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractor objects
        distractors = ['calculator', 'screwdriver', 'toycar', 'red_block', 'microphone']
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - Place can and tissue-box on the coaster.
        - Place pot-with-plant on the coaster (wrong action), then recover by placing it on the table.
        - Place bread on the table.
        """
        # Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info

        # Place tissue-box on coaster
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("Place tissue-box on coaster:", success)
        if not success:
            return self.info

        # Wrongly place pot-with-plant on coaster
        success = self.pick_and_place(self.pot_with_plant, self.coaster)
        print("Wrongly place pot-with-plant on coaster:", success)
        if not success:
            return self.info

        # Recover by placing pot-with-plant on the table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Place pot-with-plant on table:", success)
        if not success:
            return self.info

        # Place bread on the table
        success = self.pick_and_place(self.bread, self.table)
        print("Place bread on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Can and tissue-box must be on the coaster.
        - Pot-with-plant and bread must be on the table (not on the coaster).
        """
        can_on_coaster = self.check_on(self.can, self.coaster)
        tissue_on_coaster = self.check_on(self.tissue_box, self.coaster)
        pot_on_table = self.check_on(self.pot_with_plant, self.table)
        bread_on_table = self.check_on(self.bread, self.table)

        return can_on_coaster and tissue_on_coaster and pot_on_table and bread_on_table
