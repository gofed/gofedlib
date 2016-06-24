import unittest
from graphutils import Graph, GraphUtils

class GraphUtilsTest(unittest.TestCase):

	def _assertGraphsEqual(self, g1, g2):
		# nodes match
		self.assertEqual(g1.nodes(), g2.nodes())

		# edges match
		self.assertEqual(g1.edges(), g2.edges())


	def test_newGraph(self):
		nodes = set([2,1,3,4,5])
		edges = {1:set([1]), 2:set([2]), 3:set([4,5])}
		g = Graph(nodes, edges)

		# nodes match
		self.assertEqual(g.nodes(), nodes)

		# edges match
		self.assertEqual(g.edges(), edges)

	def test_utilsEdges2AdjacentList(self):

		edges = set([(1,2), (2,3), (3,4)])

		a_edges = GraphUtils.edges2adjacentList(edges)
		e_edges = {1: set([2]), 2: set([3]), 3: set([4])}

		self.assertEqual(a_edges, e_edges)

	def test_transposeGraph(self):

		nodes = set([1,2,3,4])
		edges = {1: set([2]), 2: set([3]), 3: set([4])}

		g = Graph(nodes, edges)

		t_g = GraphUtils.transposeGraph(g)

		e_edges = {2: set([1]), 3: set([2]), 4: set([3])}

		self._assertGraphsEqual(t_g, Graph(nodes, e_edges))

	def test_getLeafNodes(self):

		nodes = set([1,2,3,4,5])
		edges = {1: set([2]), 2: set([3,5]), 3: set([4])}

		g = Graph(nodes, edges)

		e_nodes = set([4,5])

		self.assertEqual(GraphUtils.getLeafNodes(g), e_nodes)

	def test_getRootNodes(self):

		nodes = set([1,2,3,4,5])
		edges = {1: set([2]), 2: set([3,5]), 4: set([2])}

		g = Graph(nodes, edges)

		e_nodes = set([1,4])

		self.assertEqual(GraphUtils.getRootNodes(g), e_nodes)

	def test_joinGraphs(self):

		nodes = set([1,2,3])
		edges = {1: set([2]), 2: set([3]), 3: set([3])}

		g1 = Graph(nodes, edges)

		nodes = set([3,4,5])
		edges = {3: set([4]), 4: set([5]), 5: set([4])}

		g2 = Graph(nodes, edges)

		j_g = GraphUtils.joinGraphs(g1, g2)

		e_nodes = set([1,2,3,4,5])
		e_edges = {1: set([2]), 2: set([3]), 3: set([3,4]), 4: set([5]), 5: set([4])}

		self._assertGraphsEqual(j_g, Graph(e_nodes, e_edges))

	def test_scc(self):
		nodes = set([1,2,3,4,5])
		edges = {1: set([2]), 2: set([3,5]), 3: set([1]), 4: set([2]), 5: set([5])}
		g = Graph(nodes, edges)

		e_sccs = set([frozenset([1,2,3]), frozenset([5])])

		self.assertEqual(GraphUtils.getSCCs(g), e_sccs)

	def test_getReacheableSubgraph(self):

		nodes = set([1,2,3,4,5])
		edges = {1: set([2]), 2: set([3,5]), 3: set([1]), 4: set([2]), 5: set([5])}
		g = Graph(nodes, edges)

		e_nodes = set([1,2,3,5])
		e_edges = {1: set([2]), 2: set([3,5]), 3: set([1]), 5: set([5])}

		r_g = GraphUtils.getReacheableSubgraph(g, 1)

		self._assertGraphsEqual(r_g, Graph(e_nodes, e_edges))

	def test_truncateGraph(self):

		nodes = set([1,2,3,4,5])
		edges = {1: set([2]), 2: set([3,2]), 3: set([1]), 4: set([2]), 5: set([5])}
		g = Graph(nodes, edges)

		e_nodes = set([1,2,3,5])
		e_edges = {1: set([2]), 2: set([3,2]), 3: set([1]), 5: set([5])}

		t_g = GraphUtils.truncateGraph(g, [1, 5])

		self._assertGraphsEqual(t_g, Graph(e_nodes, e_edges))

