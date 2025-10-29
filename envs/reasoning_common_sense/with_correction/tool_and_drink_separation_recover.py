
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class tool_and_drink_separation_recover(Imagine_Task):
    def load_actors(self):
        # Containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.plate = self.add_actor("plate", "plate")

        # Objects: tools and drinks
        self.hammer = self.add_actor("hammer", "hammer")
        self.microphone = self.add_actor("microphone", "microphone")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup = self.add_actor("cup_without_handle", "cup_without_handle")

        print("load actor")

    def play_once(self):
        self.save_camera_rgb("/home/wangzhuoran/RoboTwin/data/first_img.png",'front_camera')
        # Mistake: place bottle on plate (should be wooden_box), then recover
        success = self.pick_and_place(self.bottle, self.plate)
        print("mistake bottle->plate:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("recover bottle->wooden_box:", success)
        if not success:
            return self.info

        # Correct: place cup into wooden_box
        success = self.pick_and_place(self.cup, self.wooden_box)
        print("place cup->wooden_box:", success)
        if not success:
            return self.info

        # Mistake: place hammer into wooden_box, then recover to plate
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("mistake hammer->wooden_box:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.hammer, self.plate)
        print("recover hammer->plate:", success)
        if not success:
            return self.info

        # Correct: place microphone on plate
        success = self.pick_and_place(self.microphone, self.plate)
        print("place microphone->plate:", success)
        if not success:
            return self.info

    def check_success(self):
        # Drinks in wooden_box; tools on plate
        return (
            self.check_on(self.bottle, self.wooden_box)
            and self.check_on(self.cup, self.wooden_box)
            and self.check_on(self.hammer, self.plate)
            # and self.check_on(self.microphone, self.plate)
        )
