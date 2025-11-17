from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 117_protect_surface_place_drinkware_and_fragile_items(Imagine_Task):
    def load_actors(self):
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")

        # Add the required objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.microphone = self.add_actor("microphone", "microphone")

        # Add distractors
        distractor_list = ["apple", "baguette", "toycar", "red_block", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # Place sand-clock on coaster
        success = self.pick_and_place(self.sand_clock, self.coaster)
        print("Place sand-clock on coaster:", success)
        if not success:
            return self.info

        # Wrongly place screwdriver on coaster
        success = self.pick_and_place(self.screwdriver, self.coaster)
        print("Wrongly place screwdriver on coaster:", success)
        if not success:
            return self.info

        # Recovery: move screwdriver to table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Recover screwdriver to table:", success)
        if not success:
            return self.info

        # Place hammer on table
        success = self.pick_and_place(self.hammer, self.table)
        print("Place hammer on table:", success)
        if not success:
            return self.info

        # Place microphone on table
        success = self.pick_and_place(self.microphone, self.table)
        print("Place microphone on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check that drinkware and fragile items are on the coaster
        on_coaster = (
            self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.sand_clock, self.coaster)
        )

        # Check that heavy tools and electronic devices are on the table
        on_table = (
            self.check_on(self.screwdriver, self.table) and
            self.check_on(self.hammer, self.table) and
            self.check_on(self.microphone, self.table)
        )

        return on_coaster and on_table
