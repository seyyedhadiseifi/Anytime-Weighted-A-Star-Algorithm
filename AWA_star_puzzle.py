'''
Created on Oct 10, 2018

@author: ss4350
'''

import numpy as np
import copy
import time
import queue as Q


class NodeClass:
    w = 3
    status = ''

    def __init__(self, content, predecessor, goal):
        self.content = content
        self.f = 0  # admissible
        self.fp = 0  # non-admissible
        self.g = 0  # cost function
        self.h = 0  # heuristic function
        self.predecessor = predecessor
        self.size = self.content.shape[0]
        self.goal = goal

    def is_goal(self):
        if np.array_equal(self.content, self.goal):
            return True
        else:
            return False

    def calculate_h(self):
        h_value = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.goal[i, j] != self.size ** 2 and self.content[i, j] != self.goal[i, j]:
                    a, b = np.where(self.content == self.goal[i, j])
                    h_value += abs(a[0] - i) + abs(b[0] - j)
        self.h = h_value

    def calculate_g(self):
        # g value
        parent = self.predecessor
        self.g = parent.g + 1

    def calculate_f(self):
        # f value
        self.fp = self.g + self.w * self.h
        self.f = self.g + self.h

    def calculate_costs(self):
        self.calculate_h()
        self.calculate_g()
        self.calculate_f()

    def __str__(self):
        output = ''
        output += 'fp(%0.2f) = g(%0.2f) + %0.1f*h(%0.2f)\n' % (self.fp, self.g, self.w, self.h)
        output += 'f (%0.2f) = g(%0.2f) + h(%0.2f)\n' % (self.f, self.g, self.h)
        for i in range(self.size):
            for j in range(self.size):
                if self.content[i, j] == self.size ** 2:
                    output += '%2s' % 'b'
                else:
                    output += '%2d' % self.content[i, j]
                output += ' '
            output += '\n'
        return output

    def __eq__(self, other):
        if np.array_equal(self.content, other.content):
            return True
        else:
            return False

    def generate_successor(self):
        successors_list = []

        content = self.content
        i, j = np.where(content == self.size ** 2)
        i = i[0]
        j = j[0]

        # Move blank up
        if i != 0:
            temp = copy.deepcopy(content)
            temp_value = temp[i - 1][j]
            temp[i - 1][j] = self.size ** 2
            temp[i][j] = temp_value
            successors_list.append(NodeClass(temp, self, self.goal))

        # Move blank down
        if i != (content.shape[0] - 1):
            temp = copy.deepcopy(content)
            temp_value = temp[i + 1][j]
            temp[i + 1][j] = self.size ** 2
            temp[i][j] = temp_value
            successors_list.append(NodeClass(temp, self, self.goal))

        # Move blank left
        if j != 0:
            temp = copy.deepcopy(content)
            temp_value = temp[i][j - 1]
            temp[i][j - 1] = self.size ** 2
            temp[i][j] = temp_value
            successors_list.append(NodeClass(temp, self, self.goal))

        # Move blank right
        if j != (content.shape[1] - 1):
            temp = copy.deepcopy(content)
            temp_value = temp[i][j + 1]
            temp[i][j + 1] = self.size ** 2
            temp[i][j] = temp_value
            successors_list.append(NodeClass(temp, self, self.goal))

        return successors_list

    def build_path(self):
        path = [self]
        current = self
        while current.predecessor.status == '':
            path.append(current.predecessor)
            current = current.predecessor
        path.append(current.predecessor)

        return path


def shuffle_board(board, n):
    temp = copy.deepcopy(board)
    for i in range(n):
        # random direction
        direction = np.random.choice(range(4), 1)
        a, b = np.where(temp == board.shape[0] ** 2)
        a = a[0]
        b = b[0]
        # Move blank up
        if direction == 0 and a != 0:
            temp_value = temp[a - 1][b]
            temp[a - 1][b] = temp.shape[0] ** 2
            temp[a][b] = temp_value

        # Move blank down
        if direction == 1 and a != board.shape[0] - 1:
            temp_value = temp[a + 1][b]
            temp[a + 1][b] = board.shape[0] ** 2
            temp[a][b] = temp_value

        # Move blank left
        if direction == 2 and b != 0:
            temp_value = temp[a][b - 1]
            temp[a][b - 1] = board.shape[0] ** 2
            temp[a][b] = temp_value

        # Move blank right
        if direction == 3 and b != board.shape[0] - 1:
            temp_value = temp[a][b + 1]
            temp[a][b + 1] = board.shape[0] ** 2
            temp[a][b] = temp_value

    return temp


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


# 8-Puzzle
goal = np.array([[1, 2, 3], [8, 9, 4], [7, 6, 5]])
# goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# 15-Puzzle
# goal = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])

# Shuffle
# startNode = shuffle_board(goal, 8000)
startNode = np.array([[5, 6, 7], [4, 9, 8], [3, 2, 1]])
startNode = np.array([[8, 6, 7], [2, 5, 4], [3, 9, 1]])

startNode = NodeClass(startNode, 0, goal)
startNode.status = 'Start'
startNode.calculate_h()
startNode.calculate_f()
print('Start Node')
print(startNode)

open_list = [startNode]
closed_list = []
start_time = time.time()

upper_bound = None

# for i in range(2):
while len(open_list) != 0:
    # Find node with least f
    node = get_min(open_list)
    # print 'Min Node is:------------------------------------------------'
    # print node
    # print 'O:%d, C:%d' % (len(open_list), len(closed_list))

    open_list.remove(node)

    if upper_bound is None or node.f < upper_bound.f:
        # Add to closed list
        closed_list.append(node)

        # Generate successors
        successors = node.generate_successor()

        # Iterate over children
        for s in successors:
            # Calculate costs and compare with upper bound
            s.calculate_costs()

            # print temp[j]
            if upper_bound is not None and s.f >= upper_bound.f:
                continue

            # Check if successor is the goal node
            if s.is_goal():
                # update upper bound
                upper_bound = s
                print('New Upper Bound:****************************************************')
                print('Total time is: %5f' % (time.time() - start_time))
                print(upper_bound)
                print('')

            # Check for better duplicates in open_list
            elif s in open_list:
                k = open_list.index(s)
                if s.g >= open_list[k].g:
                    continue
                else:
                    open_list.remove(s)
                    open_list.append(s)

            # Check for better duplicates in closed_list
            elif s in closed_list:
                k = closed_list.index(s)
                if s.g >= closed_list[k].g:
                    continue
                else:
                    closed_list.remove(s)
                    open_list.append(s)
            else:
                open_list.append(s)

path_to_start = upper_bound.build_path()
print('Number of moves: %d' % upper_bound.g)
print('path is:****************************************************')

for item in reversed(path_to_start):
    print(item)
print('Total time is: %5f' % (time.time() - start_time))
