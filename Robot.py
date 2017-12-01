from Actor import Actor
import random

class Robot(Actor):
    def __init__(self, location, grid, instructions):
        Actor.__init__(self, location, grid, icon="robot.gif")
        file = open(instructions, "r")
        actions = file.read().split("\n")
        actions[:] = [action for action in actions if action.strip() != ""]
        self.main_loop = Loop(1, actions, self)
        self.variables = {}
        self.variables["row"] = self.location.row
        self.variables["col"] = self.location.col

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
        elif action is None:
            pass
        else:
            print("Unknown action: " + action)
        self.location.row = round(self.variables["row"])
        self.location.col = round(self.variables["col"])

    def move_to(self, location):
        # if self.grid.is_valid(location):
        Actor.move_to(self, location)
        self.variables["row"] = self.location.row
        self.variables["col"] = self.location.col

    def get_value(self, variable):
        if variable is None:
            return None
        if type(variable) is not str:
            return variable
        if index_of(variable, "==") != -1:
            stripped = "".join(variable.split())
            equals_index = index_of(stripped, "==")
            row = stripped[:equals_index]
            col = stripped[equals_index + 2:]
            return self.get_value(row) == self.get_value(col)
        elif variable[0] == "\"" and variable[-1] == "\"":
            return variable[1:-1]
        elif variable == "random()":
            return random.random()
        elif variable == "True":
            return True
        elif variable == "False":
            return False
        elif variable == "can move":
            return self.can_move(self.direction)
        elif variable == "direction":
            return self.direction
        else:
            try:
                return float(variable)
            except ValueError:
                try:
                    return self.variables[variable]
                except KeyError:
                    variable = variable.strip()
                    expression = Expression()
                    component = ""
                    for char in variable:
                        if char == "^" or char == "/" or char == "*" or char == "%" or char == "+" or char == "-":
                            if component is not "":
                                expression.add_node(Node(component, self))
                            expression.add_node(Node(char, self))
                            component = ""
                        else:
                            component += char
                    if component is not "":
                        expression.add_node(Node(component, self))
                    try:
                        return expression.eval()
                    except KeyError:
                        print("Unable to interpret expression: " + variable)


class Expression:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_node(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.right = node
            node.left = self.tail
            self.tail = node

    def eval(self):
        while self.head.right is not None:
            iter_node = self.head
            top_priority = None
            top_priority_node = None
            while iter_node is not None:
                priority = iter_node.priority
                if priority is not None and (top_priority is None or priority < top_priority):
                    top_priority = priority
                    top_priority_node = iter_node
                iter_node = iter_node.right
            value = top_priority_node.get_value()
            new_node = Node(value, top_priority_node.robot)
            try:
                top_priority_node.right.right.left = new_node
                new_node.right = top_priority_node.right.right
            except AttributeError:
                self.tail = new_node
            try:
                top_priority_node.left.left.right = new_node
                new_node.left = top_priority_node.left.left
            except AttributeError:
                self.head = new_node
        return self.head.get_value()

    def __str__(self):
        string = ""
        iter_node = self.head
        while iter_node is not None:
            string += str(iter_node.value) + "(" + str(iter_node.priority) + ") "
            iter_node = iter_node.right
        return string

class Node:
    def __init__(self, value, robot, left=None, right=None):
        self.value = value
        self.priority = None
        if self.value == "^":
            self.priority = 0
        if self.value == "*" or self.value == "/" or self.value == "%":
            self.priority = 1
        if self.value == "+" or self.value == "-":
            self.priority = 2
        self.robot = robot
        assert(type(robot) is Robot)
        self._left = left
        self._right = right

    def get_value(self):
        if self.priority is not None:
            if self.value == "^":
                return eval(str(self.left.get_value()) + "**" + str(self.right.get_value()))
            return eval(str(self.left.get_value()) + str(self.value) + str(self.right.get_value()))
        return self.robot.get_value(self.value)

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right


class Loop:
    def __init__(self, loop_amount, actions, robot, condition="False"):
        self.loop_amount = loop_amount
        self.action_index = 0
        self.actions = actions
        self.loop = None
        self.robot = robot
        self.condition = condition

    def __str__(self):
        return str(self.actions) + " sub-loop[" + str(self.loop) + "] + i:" + str(self.action_index) + " c:" + str(
            self.loop_amount)

    def next_action(self):
        """Returns the next action to do and increments action index"""
        action = None
        # If we're currently reading from a sub-loop, get that loop's action
        if self.loop is not None:
            action = self.loop.next_action()
            if action is None:
                self.loop = None

        # If we don't have to do anything from a sub loop and we're not at the end of our loop
        if action is None and self.action_index < len(self.actions):
            # Get the next action and increment the action index
            action = self.actions[self.action_index]
            self.action_index += 1
        # Else, we're at the end of our loop
        elif self.action_index == len(self.actions) and self.loop is None:
            self.loop_amount -= 1
            # If we still have to keep looping
            # print (self, self.condition, self.robot.get_value(self.condition))
            if self.loop_amount > 0 or self.robot.get_value(self.condition):
                # Reset the action index to the top of the loop and get the next action from that index
                self.action_index = 0
                action = self.next_action()

        heading = self.get_heading(action)
        if heading is not None:
            if heading.type == "=":
                assignment = self.robot.get_value(heading.assignment)
                self.robot.variables[heading.variable] = assignment
                return self.next_action()
            elif heading.type == "loop":
                self.loop = Loop(heading.loop_amount, heading.subcode, self.robot)
                # Update the sub-loop and then return the next action with this new sub-loop
                return self.next_action()
            elif heading.type == "if":
                if self.robot.get_value(heading.condition):
                    self.loop = Loop(1, heading.subcode, self.robot)
                elif heading.else_subcode is not None:
                    self.loop = Loop(1, heading.else_subcode, self.robot)
                return self.next_action()
            elif heading.type == "while":
                self.loop = Loop(0, heading.subcode, self.robot, condition=heading.condition)
                return self.next_action()
            elif heading.type == "print":
                print(heading.arguments[0])
                return self.next_action()
        else:
            return action

    def get_heading(self, action):
        if index_of(action, "=") != -1 and index_of(action, "==") == -1:
            stripped = "".join(action.split())
            equals_index = index_of(stripped, "=")
            variable = stripped[:equals_index]
            assignment = self.robot.get_value(stripped[equals_index + 1:])
            return Heading("=", variable=variable, assignment=assignment)
        elif index_of(action, "loop") != -1:
            try:
                return Heading("loop", loop_amount=int(action[5:-1]), subcode=self.get_subcode())
            except ValueError:
                print("ValueError: '" + action[5:-1] + "' isn't a valid number")
        elif index_of(action, "if") != -1:
            if_subcode = self.get_subcode()
            else_subcode = None
            if len(self.actions) > self.action_index and self.actions[self.action_index].strip() == "else:":
                self.action_index += 1
                else_subcode = self.get_subcode()
            return Heading("if", condition=action[3:-1], subcode=if_subcode, else_subcode=else_subcode)
        elif index_of(action, "while") != -1:
            return Heading("while", condition=action[6:-1], subcode=self.get_subcode())
        elif index_of(action, "print") != -1:
            stripped = "".join(action.split())
            args = [self.robot.get_value(stripped[6:-1])]
            return Heading("print", arguments=args)
        else:
            return None

    def get_subcode(self):
        sub_loop_actions = []
        tab_str = "    "
        try:
            index_of_tab = self.actions[self.action_index].index(tab_str)
        except ValueError:
            index_of_tab = -1
        # Add all the actions in the new sub-loop to that sub-loop's action list
        while self.action_index < len(self.actions) and (
                        index_of_tab == 0 or self.actions[self.action_index].strip() == ""):
            if not self.actions[self.action_index].strip() == "":
                sub_loop_actions.append(self.actions[self.action_index][len(tab_str):])
            self.action_index += 1
            try:
                index_of_tab = self.actions[self.action_index].index(tab_str)
            except (IndexError, ValueError):
                index_of_tab = -1
        return sub_loop_actions


class Heading:
    def __init__(self, type, condition=None, subcode=None, else_subcode=None, loop_amount=None, variable=None,
                 assignment=None, arguments=None):
        self.type = type
        self.condition = condition
        self.subcode = subcode
        self.else_subcode = else_subcode
        self.loop_amount = loop_amount
        self.variable = variable
        self.assignment = assignment
        self.arguments = arguments


def index_of(big_string, target):
    if big_string is None or target is None:
        return -1
    target_index = 0
    target_len = len(target)
    congruency_count = 0
    index = -1

    for i, char in enumerate(big_string):
        if char == target[target_index]:
            if index == -1:
                index = i
            congruency_count += 1
            target_index += 1
            if congruency_count == target_len:
                return index
        else:
            congruency_count = 0
            target_index = 0
            index = -1
    return index
