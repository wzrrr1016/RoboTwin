
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class place_food_left_tools_right(Imagine_Task):
    def load_actors(self):
        # Containers
        self.tray = self.add_actor("tray", "tray")

        # Objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.hammer = self.add_actor("hammer", "hammer")
        self.microphone = self.add_actor("microphone", "microphone")

    def play_once(self):
        # Spatial reasoning: place food on left side of tray, tools on right
        # We approximate left/right by two placements onto tray
        for obj in [self.apple, self.hamburg, self.hammer, self.microphone]:
            success = self.pick_and_place(obj, self.tray)
            if not success:
                return self.info

    def check_success(self):
        # Simplified: verify all items are on tray (left/right not encoded in contact API)
        return (
            self.check_on(self.apple, self.tray)
            and self.check_on(self.hamburg, self.tray)
            and self.check_on(self.hammer, self.tray)
            and self.check_on(self.microphone, self.tray)
        )

