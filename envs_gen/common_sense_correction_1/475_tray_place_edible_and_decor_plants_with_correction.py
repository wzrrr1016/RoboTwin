from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 475_tray_place_edible_and_decor_plants_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the tray, edible items, decorative plants, sharp utensils, and repair tools.
        Distractors are also added to the environment.
        """
        # Add the tray as the main container
        self.tray = self.add_actor("tray", "tray")

        # Add edible items
        self.bread = self.add_actor("bread", "bread")

        # Add sharp utensils
        self.knife = self.add_actor("knife", "knife")

        # Add repair tools
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add decorative plants
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractors to the environment
        distractor_list = ["calculator", "toycar", "alarm-clock", "small-speaker", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot arm should perform.
        The robot places edible items and decorative plants on the tray,
        and places sharp utensils and repair tools on the table.
        """
        # Step 1: Place bread on the tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Place bread on tray:", success)
        if not success:
            return self.info

        # Step 2: Place screwdriver on the tray (wrong action)
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Place screwdriver on tray (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing screwdriver on the table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Place screwdriver on table (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place pot-with-plant on the tray
        success = self.pick_and_place(self.pot_with_plant, self.tray)
        print("Place pot-with-plant on tray:", success)
        if not success:
            return self.info

        # Step 5: Place knife on the table
        success = self.pick_and_place(self.knife, self.table)
        print("Place knife on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        Success is defined as:
        - Bread and pot-with-plant are on the tray
        - Knife and screwdriver are on the table
        """
        # Check if edible items and decorative plants are on the tray
        bread_on_tray = self.check_on(self.bread, self.tray)
        pot_on_tray = self.check_on(self.pot_with_plant, self.tray)

        # Check if sharp utensils and repair tools are on the table
        knife_on_table = self.check_on(self.knife, self.table)
        screwdriver_on_table = self.check_on(self.screwdriver, self.table)

        # Return True only if all conditions are met
        return bread_on_tray and pot_on_tray and knife_on_table and screwdriver_on_table
