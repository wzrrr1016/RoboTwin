from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class timekeeping_device_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load the plate and shoe box actors
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Load the timekeeping devices and other objects
        self.timekeeping_devices = [
            self.add_actor("alarm-clock", "alarm-clock"),
            self.add_actor("sand-clock", "sand-clock")
        ]
        self.other_objects = [
            self.add_actor("scanner", "scanner"),
            self.add_actor("book", "book")
        ]

    def play_once(self):
        # Pick and place the timekeeping devices into the plate
        for device in self.timekeeping_devices:
            success = self.pick_and_place(device, self.plate)
            if not success:
                return self.info

        # Pick the sand-clock from the plate and place it into the shoe box
        sand_clock_on_plate = self.check_on(self.timekeeping_devices[1], self.plate)
        if sand_clock_on_plate:
            success = self.pick_and_place(self.timekeeping_devices[1], self.shoe_box)
            if not success:
                return self.info

        # Pick and place the scanner and book into the shoe box
        for obj in self.other_objects:
            success = self.pick_and_place(obj, self.shoe_box)
            if not success:
                return self.info

    def check_success(self):
        # Check if all timekeeping devices are on the plate
        for device in self.timekeeping_devices:
            if not self.check_on(device, self.plate):
                return False

        # Check if the sand-clock is in the shoe box
        if not self.check_on(self.timekeeping_devices[1], self.shoe_box):
            return False

        # Check if all other objects are in the shoe box
        for obj in self.other_objects:
            if not self.check_on(obj, self.shoe_box):
                return False

        return True

# Example usage:
# task = PlaceObjectsTask()
# task.load_actors()
# task.play_once()
# success = task.check_success()
# print("Task completed successfully:", success)
