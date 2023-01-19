from heapq import heappush, heappop
import numpy as np

key = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
inv_key = {v: k for k, v in key.items()}

class AStar():
  def __init(self, nodes, start, goal):
    self.start = start
    self.goal = goal
    self.heap = []
    self.path = {}
    self.g_score = dict.fromkeys(nodes, np.inf)
    self.g_score[start] = 0
    self.f_score = {}
    self.f_score[start] = self.__calculate_f_score(start)
    heappush(self.heap, (self.f_score[start], start))

  def __calculate_f_score(self, node):
    # Use manhattan distance as our admissible heuristic
    h_score = np.sum(np.abs(np.array(node) - self.goal))
    return self.g_score[node] + h_score

  def __get_neighbours(self, node):
    neighbours = []
    for v in key.values():
      n = tuple(np.array(node) + v)
      if self.g_score.get(n):
        neighbours.append(n)
    return neighbours

  def __reconstruct_route(self):
    route = []
    current = self.goal
    while current != self.start:
      step = tuple(np.array(current) - self.path[current])
      print(step, inv_key[step])
      route.append(inv_key[step])
      current = self.path[current]
    route.reverse()
    return ''.join(route)

  def solve(self, nodes, start, goal):
    self.__init(nodes, start, goal)
    while self.heap:
      _, current = heappop(self.heap)
      if current == self.goal:
        return self.__reconstruct_route()
      for n in self.__get_neighbours(current):
        potential = self.g_score[current] + 1
        if potential < self.g_score.get(n, np.inf):
          self.path[n] = current
          self.g_score[n] = self.g_score[current] + 1
          self.f_score[n] = self.__calculate_f_score(n)
          if (self.f_score[n], n) not in self.heap:
            heappush(self.heap, (self.f_score[n], n))
    return False
