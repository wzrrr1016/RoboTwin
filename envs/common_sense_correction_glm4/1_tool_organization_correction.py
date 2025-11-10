from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class tool_organization_correction(Imagine_Task):
    def load_actors(self):
        self.tray = self.add_actor("tray", "tray")
        self.coaster = self.add_actor("coaster", "coaster")

        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.pot_with_plant = self.add_actor("pot_with_plant", "pot_with_plant")
        self.book = self.add_actor("book", "book")

    def play_once(self):
        # Pick up the hammer and place it into the tray.
        success = self.pick_and_place(self.hammer, self.tray)
        print("Pick and place hammer:", success)
        if not success:
            return self.info

        # Attempt to pick up the screwdriver and place it into the tray.
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Pick and place screwdriver (wrong):", success)
        if not success:
            return self.info

        # Pick up the screwdriver from the tray and place it onto the coaster.
        success = self.pick_and_place(self.screwdriver, self.coaster)
        print("Pick and place screwdriver (recovery):", success)
        if not success:
            return self.info

        # Pick up the pot-with-plant and place it onto the coaster.
        success = self.pick_and_place(self.pot_with_plant, self.coaster)
        print("Pick and place pot-with-plant:", success)
        if not success:
            return self.info

        return "All tasks completed successfully."

    def check_success(self):
        # Check if the hammer is on the tray.
        if not self.check_on(self.hammer, self.tray):
            return False

        # Check if the screwdriver is on the coaster.
        if not self.check_on(self.screwdriver, self.coaster):
            return False

        # Check if the pot-with-plant is on the coaster.
        if not self.check_on(self.pot_with_plant, self.coaster):
            return False

        return True