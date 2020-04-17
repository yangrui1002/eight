# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time     : 2020/4/15 8:26
# @Author   : yangrui
"""
import copy
import heapq
import random
from collections import deque

distance = [[0, 2, 1, 2, 1, 2, 1, 2, 1],
            [2, 0, 1, 2, 3, 4, 3, 2, 1],
            [1, 1, 0, 1, 2, 3, 2, 3, 2],
            [2, 2, 1, 0, 1, 2, 3, 4, 3],
            [1, 3, 2, 1, 0, 1, 2, 3, 2],
            [2, 4, 3, 2, 1, 0, 1, 2, 3],
            [1, 3, 2, 3, 2, 1, 0, 1, 2],
            [2, 2, 3, 4, 3, 2, 1, 0, 1],
            [1, 1, 2, 3, 2, 3, 2, 1, 0]]
follow = {0: [1, 2], 1: [2, 5], 2: [5, 8], 3: [0, 1], 4: -1, 5: [8, 7], 6: [3, 0], 7: [6, 3], 8: [7, 6]}
target = [1, 2, 3, 8, 0, 4, 7, 6, 5]
move = [('u', -1, 0), ('d', 1, 0), ('l', 0, -1), ('r', 0, 1)]

class My_PriorityQueue(object):
    def __init__(self):
        self.__queue = []
        self.__index = 0
    def push(self, item, priority):
        heapq.heappush(self.__queue, (priority, self.__index, item))
        self.__index += 1
    def pop(self):
        return heapq.heappop(self.__queue)[-1]
    def empty(self):
        return True if not self.__queue else False

def cost1(src):
    sum = 0
    for index, value in enumerate(target):
        if src[index] != value:
            sum += 1
    return sum
def cost2(src):
    sum = 0
    for index, value in enumerate(target):
        if src[index] != 0:
            sum += distance[src[index]][value]
    return sum
def cost3(src):
    sum = 0
    for index, value in enumerate(target):
        if src[index] != 0:
            sum += distance[src[index]][value]
            if index == 4:
                sum += 3
            elif src[follow[index][0]] != 0:
                if src[index] % 8 != src[follow[index][0]] - 1:
                    sum += 6
            elif src[index] % 8 != src[follow[index][1]] - 1:
                sum += 6
    return sum

def insert(opened, node, method):
    if method in [1, 2]:
        opened.append(node)
    elif method == 3:
        opened.push(node, cost1(node[0]) + node[2] + 1)
    elif method == 4:
        opened.push(node, cost2(node[0]) + node[2] + 1)
    elif method == 5:
        opened.push(node, cost3(node[0]) + node[2] + 1)
def delete(opened, method):
    if method in [2, 3, 4, 5]:
        return opened.pop()
    elif method == 1:
        return opened.popleft()
def is_empty(opened, method):
    if method in [1, 2]:
        return True if not opened else False
    elif method in [3, 4, 5]:
        return opened.empty()

def search(src, opened, method):
    closed = set([])
    e_num, c_num = 0, 0
    loc = src.index(0)
    head = (src, loc, 0, '')
    insert(opened, head, method)
    c_num += 1
    while not is_empty(opened, method):
        cur = delete(opened, method)
        e_num += 1
        print('探索第 ', c_num, ' 个节点:', cur[0])
        if cur[0] == target:
            print('生成了', c_num, '个节点')
            print('扩展了', e_num, '个节点')
            print('该问题的解为:', cur[3])
            return c_num, e_num, cur[3]
        if tuple(cur[0]) not in closed:
            tx, ty = cur[1] // 3, cur[1] % 3
            for d, mx, my in move:
                x, y = tx + mx, ty + my
                if (x < 0 or x > 2 or y < 0 or y > 2):
                    continue
                next = copy.deepcopy(cur[0])
                nloc = x * 3 + y
                next[cur[1]], next[nloc] = next[nloc], next[cur[1]]
                if tuple(next) not in closed:
                    insert(opened, (next, nloc, cur[2] + 1, cur[3] + d), method)
                    c_num += 1
        closed.add(tuple(cur[0]))

def BFS(src):
    opened = deque([])
    return search(src, opened, 1)
def DFS(src):
    opened = deque([])
    return search(src, opened, 2)
def BFS_W(src):
    opened = My_PriorityQueue()
    return search(src, opened, 3)
def BFS_P(src):
    opened = My_PriorityQueue()
    return search(src, opened, 4)
def BFS_S(src):
    opened = My_PriorityQueue()
    return search(src, opened, 5)

def sovle(src):
    ans = 0
    if set(src) != {0,1,2,3,4,5,6,7,8}:
        return False
    for i in range(len(src)):
        for j in range(i):
            if src[j] > src[i] and src[i] != 0 and src[j] != 0:
                ans += 1
    return True if ans%2==1 else False

def generator():
    src = random.sample(range(9), 9)
    while not sovle(src):
        src = random.sample(range(9), 9)
    return src

if __name__ == '__main__':
    S = generator()
    print(sovle(S))
    BFS_S(S)
