from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class organize_natural_perishables_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the container (fluted_block), the target objects,
        and the distractors.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the target objects
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.drill = self.add_actor("drill", "drill")

        # Add distractors
        distractor_list = ["calculator", "alarm-clock", "shoe", "book", "toycar", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        This includes placing natural and perishable items on the organizer,
        placing a tool (drill) incorrectly, and then recovering it to the table.
        """
        # Place pot-with-plant on the organizer
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Place pot-with-plant:", success)
        if not success:
            return self.info

        # Place apple on the organizer
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info

        # Wrongly place drill on the organizer
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Wrongly place drill:", success)
        if not success:
            return self.info

        # Recover drill to the table
        success = self.pick_and_place(self.drill, self.table)
        print("Recover drill to table:", success)
        if not success:
            return self.info

        # Place french fries on the organizer
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        This includes verifying that:
        - All natural and perishable items are on the organizer (fluted_block)
        - The tool (drill) is not on the organizer, but on the table
        """
        # Check if all natural/perishable items are on the organizer
        items_on_organizer = (
            self.check_on(self.pot_with_plant, self.fluted_block) and
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.french_fries, self.fluted_block)
        )

        # Check if the drill is on the table (not on the organizer)
        drill_on_table = self.check_on(self.drill, self.table)

        return items_on_organizer and drill_on_table
