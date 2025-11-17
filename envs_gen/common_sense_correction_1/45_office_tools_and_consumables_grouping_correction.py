from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 45_office_tools_and_consumables_grouping_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.tray = self.add_actor("tray", "tray")

        # Add task-specific objects
        self.markpen = self.add_actor("markpen", "markpen")
        self.stapler = self.add_actor("stapler", "stapler")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.french_fries = self.add_actor("french_fries", "french_fries")

        # Add distractors
        distractor_list = ["pot-with-plant", "alarm-clock", "toycar", "sand-clock", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        """
        # Place small office supplies and hand tools into fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Pick place markpen:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Pick place stapler:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Pick place screwdriver:", success)
        if not success:
            return self.info

        # Wrong placement of shampoo (recovery needed)
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Pick place shampoo (wrong):", success)
        if not success:
            return self.info

        # Recovery: Move shampoo to tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick place shampoo (recovery):", success)
        if not success:
            return self.info

        # Place consumable food item on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Pick place french fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if all objects are placed in the correct containers.
        """
        # Check if office supplies and hand tools are in fluted_block
        office_supplies_in_fluted_block = (
            self.check_on(self.markpen, self.fluted_block) and
            self.check_on(self.stapler, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block)
        )

        # Check if consumables are on tray
        consumables_on_tray = (
            self.check_on(self.shampoo, self.tray) and
            self.check_on(self.french_fries, self.tray)
        )

        return office_supplies_in_fluted_block and consumables_on_tray
