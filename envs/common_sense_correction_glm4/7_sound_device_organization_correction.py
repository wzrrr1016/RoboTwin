from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class sound_device_organization_correction(Imagine_Task):
    def load_actors(self):
        # Load the fluted_block and shoe_box
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Load the sound-producing devices
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.bell = self.add_actor("bell", "bell")

        # Load the non-sound-producing items
        self.drill = self.add_actor("drill", "drill")
        self.bread = self.add_actor("bread", "bread")

    def play_once(self):
        # Pick up the alarm-clock and place it into the fluted_block
        success = self.pick_and_place(self.alarm_clock, self.fluted_block)
        print("Pick and place alarm-clock:", success)
        if not success:
            return self.info

        # Attempt to pick up the bell (wrong action)
        success = self.pick_and_place(self.bell, self.shoe_box)
        print("Pick and place bell (wrong action):", success)
        if not success:
            return self.info

        # Pick up the bell from the shoe_box and place it into the fluted_block (recovery)
        success = self.pick_and_place(self.bell, self.fluted_block)
        print("Pick and place bell (recovery):", success)
        if not success:
            return self.info

        # Pick up the drill and place it into the shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Pick and place drill:", success)
        if not success:
            return self.info

        # Pick up the bread and place it into the shoe_box
        success = self.pick_and_place(self.bread, self.shoe_box)
        print("Pick and place bread:", success)
        if not success:
            return self.info

        return "All tasks completed successfully."

    def check_success(self):
        # Check if the alarm-clock and bell are on the fluted_block
        alarm_clock_on_fluted_block = self.check_on(self.alarm_clock, self.fluted_block)
        bell_on_fluted_block = self.check_on(self.bell, self.fluted_block)
        # Check if the drill and bread are on the shoe_box
        drill_on_shoe_box = self.check_on(self.drill, self.shoe_box)
        bread_on_shoe_box = self.check_on(self.bread, self.shoe_box)

        # Return True if all conditions are met, otherwise False
        return alarm_clock_on_fluted_block and bell_on_fluted_block and drill_on_shoe_box and bread_on_shoe_box

# Example usage:
# task = OrganizeSoundDevices()
# task.load_actors()
# result = task.play_once()
# print(result)
# success = task.check_success()
# print("Success:", success)
