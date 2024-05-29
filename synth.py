from modules.oscillator import Oscillator

SAMPLE_RATE = 44100
SAMPLE_SIZE = 512

# it's a graph traversal technically using topological sort
# round robin for polyphonic synths with N voices
class Synth:
  def __init__(self) -> None:
    self.modules = {0: Oscillator(SAMPLE_RATE, SAMPLE_SIZE)}
    self.patches = {('osc', 'output'): {('fil', 'input')}}

    self.modules[0].input['CV'] = self.modules[1].output['data']

  def add_module(self, module):
    pass

  def remove_module(self, module):
    pass

  def add_patch(self, out_module, in_module, output, input):
    pass

  def remove_patch(self, out_module, in_module):
    pass

  # def topological_sort(graph):
  #     """Used to call topological sort."""
  #     stack = Stack()
  #     visited = {u: False for u in graph}
  #     for u in graph:
  #         if not visited[u]:
  #             _topological_sort(graph, u, visited, stack)
  #     while len(stack):
  #         u = stack.pop()
  #         print(u)

  # def _topological_sort(graph, u, visited, stack):
  #     """Topological sort implementation.

  #     Time Complexity: O(V + E)
  #     Space Complexity: O(V)
  #     """
  #     visited[u] = True
  #     for v in graph[u]:
  #         if not visited[v]:
  #             _topological_sort(graph, v, visited, stack)
  #     stack.push(u)
