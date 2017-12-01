from Robot import Robot
import random
from SmellyMan import SmellyMan
import math

class Sniffer(Robot):
    def act(self):
        self.variables["step"] = self.grid.step
        action = self.main_loop.next_action()
        if action == "forward":
            if self.can_move(self.direction):
                self.forward()
        elif action == "backward":
            if self.can_move(self.direction):
                self.move_to(self.get_location_in_direction(self.direction + 180))
            else:
                print("Blocked!")
        elif action == "turn right":
            self.turn_right()
        elif action == "turn left":
            self.turn_left()
        elif action == "hillclimb":
            adj_locs = self.get_empty_adjacent_locations()
            random.shuffle(adj_locs)
            max_smell = 0
            smelliest_loc = None
            for loc in adj_locs:
                smell = self.grid.smells[str(SmellyMan)][loc.row][loc.col]
                if (smell == max_smell and random.random() < 0.5) or smell > max_smell:
                    max_smell = smell
                    smelliest_loc = loc
            if smelliest_loc is not None:
                self.direction = self.get_direction_towards(smelliest_loc)
                self.move_to(smelliest_loc)

        elif action is None:
            pass
        else:
            print("Unknown action: " + action)
        self.location.row = round(self.variables["row"])
        self.location.col = round(self.variables["col"])