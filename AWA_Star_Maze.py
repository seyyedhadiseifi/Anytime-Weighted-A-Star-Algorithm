'''
Created on Oct 10, 2018

@author: ss4350
'''

import numpy as np
import copy
import time


class Location:
    w = 2

    def __init__(self, row, col, predecessor, goal):
        self.row = row
        self.col = col
        self.predecessor = predecessor
        self.goal = goal
        self.f = 0  # admissible
        self.fp = 0  # non-admissible
        self.g = 0  # cost function
        self.h = 0  # heuristic function

    def __eq__(self, other):
        if self.row == other.row and self.col == other.col:
            return True
        return False

    def calculate_h(self):
        self.h = np.sqrt(abs(self.row - self.goal.row) ** 2 + abs(self.col - self.goal.col) ** 2)

    def calculate_g(self):
        # g value
        if self.row != self.predecessor.row and self.col != self.predecessor.col:
            self.g = self.predecessor.g + 1.5
        else:
            self.g = self.predecessor.g + 1

    def calculate_f(self):
        # f value
        self.fp = self.g + self.w * self.h
        self.f = self.g + self.h

    def calculate_costs(self):
        self.calculate_h()
        self.calculate_g()
        self.calculate_f()

    def is_goal(self):
        if self.row == self.goal.row and self.col == self.goal.col:
            return True
        return False

    def __str__(self):
        return 'Row: %d, Col:%d, fp(%0.2f) = g(%0.2f) + %0.1f*h(%0.2f)' % (
            self.row, self.col, self.fp, self.g, self.w, self.h)


class Board:
    board = []

    def __init__(self, n_rows, n_cols, n_blocks):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_blocks = n_blocks

    def create_board(self):
        temp = np.zeros((self.n_rows, self.n_cols))
        np.random.seed(4)
        for i in range(self.n_blocks):
            a = np.random.choice(range(self.n_rows), 1)
            b = np.random.choice(range(self.n_cols), 1)
            if a + b != 0 and a + b != self.n_rows + self.n_cols - 2:
                temp[a, b] = 1
            else:
                continue

        self.board = temp

    def __str__(self):
        output = ''
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i, j] == 0:
                    output += '- '
                elif self.board[i, j] == 1:
                    output += '* '
                else:
                    output += 'O '
            output += '\n'
        return output


def generate_successors(node, the_board):
    successors_list = []

    # Move Up
    if node.row != 0:
        if the_board.board[node.row - 1, node.col] != 1:  # Check Barrier
            successors_list.append(Location(node.row - 1, node.col, node, node.goal))

    # Move Down
    if node.row != the_board.n_rows - 1:
        if the_board.board[node.row + 1, node.col] != 1:  # Check Barrier
            successors_list.append(Location(node.row + 1, node.col, node, node.goal))

    # Move Left
    if node.col != 0:
        if the_board.board[node.row, node.col - 1] != 1:  # Check Barrier
            successors_list.append(Location(node.row, node.col - 1, node, node.goal))

    # Move right
    if node.col != the_board.n_cols - 1:
        if the_board.board[node.row, node.col + 1] != 1:  # Check Barrier
            successors_list.append(Location(node.row, node.col + 1, node, node.goal))

    # MOve Up Right
    if node.row != 0 and node.col != the_board.n_cols - 1:
        if the_board.board[node.row - 1, node.col + 1] != 1:  # Check Barrier
            successors_list.append(Location(node.row - 1, node.col + 1, node, node.goal))

    # MOve Up Left
    if node.row != 0 and node.col != 0:
        if the_board.board[node.row - 1, node.col - 1] != 1:  # Check Barrier
            successors_list.append(Location(node.row - 1, node.col - 1, node, node.goal))

    # MOve Down Right
    if node.row != the_board.n_rows - 1 and node.col != the_board.n_cols - 1:
        if the_board.board[node.row + 1, node.col + 1] != 1:  # Check Barrier
            successors_list.append(Location(node.row + 1, node.col + 1, node, node.goal))

    # MOve Down Left
    if node.row != the_board.n_rows - 1 and node.col != 0:
        if the_board.board[node.row + 1, node.col - 1] != 1:  # Check Barrier
            successors_list.append(Location(node.row + 1, node.col - 1, node, node.goal))

    return successors_list


def get_min(temp):
    min_index = 0
    for i in range(len(temp)):
        if temp[i].fp < temp[min_index].fp:
            min_index = i

    min_index2 = min_index
    for i in range(len(temp)):
        if temp[i].fp == temp[min_index].fp:
            if temp[i].h < temp[min_index2].h:
                min_index2 = i

    return temp[min_index2]


n_row = 60
n_col = 60
n_block = 2000

board_object = Board(n_row, n_col, n_block)
board_object.create_board()
# print board_object

goal_node = Location(n_row - 1, n_col - 1, None, None)
start_node = Location(0, 0, None, goal_node)
start_node.calculate_h()
start_node.calculate_f()

open_list = [start_node]
closed_list = []

start_time = time.time()
upper_bound = None

while len(open_list) != 0:
    # Find node with least f
    node = get_min(open_list)

    # print ''
    # print 'Min Node is:------------------------------------------------'
    # print node
    # print ''

    open_list.remove(node)

    if upper_bound is None or node.f < upper_bound.f:
        # Add to closed list
        closed_list.append(node)

        # Generate successors
        successors = generate_successors(node, board_object)

        # Iterate over children
        for s in successors:
            # Calculate costs
            s.calculate_costs()

            if upper_bound is not None and s.f >= upper_bound.f:
                continue

            # Check if successor is the goal node
            if s.is_goal():
                # update upper bound
                upper_bound = s
                print('New Upper Bound:******************************************')
                print(upper_bound)
                print('Total time is: %5f' % (time.time() - start_time))
                print('')

            # Check for better duplicates in open_list
            elif s in open_list:
                k = open_list.index(s)
                # print 'In Closed with g= %0.2f' % open_list[k].g
                if s.g >= open_list[k].g:
                    continue
                else:
                    open_list.remove(s)
                    open_list.append(s)

            # Check for better duplicates in closed_list
            elif s in closed_list:
                k = closed_list.index(s)
                # print 'In Closed with g= %0.2f' % closed_list[k].g
                if s.g >= closed_list[k].g:
                    continue
                else:
                    closed_list.remove(s)
                    open_list.append(s)
            else:
                open_list.append(s)

# Modify Board to show path
print('Total time is: %5f' % (time.time() - start_time))
temp = upper_bound.predecessor
board_object.board[upper_bound.row, upper_bound.col] = 2
steps = 0
while temp is not None:
    board_object.board[temp.row, temp.col] = 2
    steps += 1
    temp = temp.predecessor
print('Number of Steps: %d' % steps)
print('')
print(board_object)
