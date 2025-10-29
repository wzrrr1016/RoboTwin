
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class tool_drink_placement(Imagine_Task):
    def load_actors(self):
        # Containers
        self.bowl = self.add_actor("bowl", "bowl")
        self.plate = self.add_actor("plate", "plate")

        # Objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.microphone = self.add_actor("microphone", "microphone")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup = self.add_actor("cup_with_handle", "cup_with_handle")

    def play_once(self):
        # Common-sense: tools on plate, drinks in bowl
        for obj, container in [
            (self.hammer, self.plate),
            (self.microphone, self.plate),
            (self.bottle, self.bowl),
            (self.cup, self.bowl),
        ]:
            success = self.pick_and_place(obj, container)
            if not success:
                return self.info

    def check_success(self):
        return (
            self.check_on(self.hammer, self.plate)
            and self.check_on(self.microphone, self.plate)
            and self.check_on(self.bottle, self.bowl)
            and self.check_on(self.cup, self.bowl)
        )

