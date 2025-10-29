
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien
import numpy as np


class split_even_odd_between_tray_bowl(Imagine_Task):
    def load_actors(self):
        # Containers
        self.tray = self.add_actor("tray", "tray")
        self.bowl = self.add_actor("bowl", "bowl")

        # Use blocks as numbered items (we encode parity in names)
        poses = self.create_box_pose(7)
        self.blocks = []
        labels = [0, 1, 2, 3, 4, 5, 7]  # mix evens and odds
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink"]
        for i, (pose, num, color) in enumerate(zip(poses, labels, colors)):
            blk = self.create_block(pose, color)
            blk.set_name(f"block_{num}")
            self.blocks.append(blk)

    def play_once(self):
        # Mistake step: place an odd block on bowl, then recover to tray
        mistake_blk = None
        for blk in self.blocks:
            num = int(blk.get_name().split("_")[-1])
            if num % 2 == 1:
                mistake_blk = blk
                break
        if mistake_blk is None:
            return self.info
        success = self.pick_place_block(mistake_blk, self.bowl)
        if not success:
            return self.info
        success = self.pick_place_block(mistake_blk, self.tray)
        if not success:
            return self.info

        # Correct: place even to bowl, odd to tray
        for blk in self.blocks:
            num = int(blk.get_name().split("_")[-1])
            target = self.bowl if num % 2 == 0 else self.tray
            success = self.pick_place_block(blk, target)
            if not success:
                return self.info

    def check_success(self):
        ok = True
        for blk in self.blocks:
            num = int(blk.get_name().split("_")[-1])
            on_bowl = self.check_actors_contact(blk, self.bowl)
            on_tray = self.check_actors_contact(blk, self.tray)
            if num % 2 == 0 and not on_bowl:
                ok = False
            if num % 2 == 1 and not on_tray:
                ok = False
        return ok

