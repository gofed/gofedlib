import json
import operator

class Graph(object):

	def __init__(self, nodes = set([]), edges = {}):
		self._nodes = nodes
		self._edges = edges

	def nodes(self):
		return self._nodes

	def edges(self):
		return self._edges

	def __str__(self):
		return json.dumps({
			"nodes": self._nodes,
			"edges": self._edges
		})

class GraphUtils(object):
	#
	# TODO(jchaloup): make all method take and return Graph type when reasonable
	#

	@staticmethod
	def edges2adjacentList(edges):
		adj_list = {}
		for (a, b) in edges:
			try:
				adj_list[a].add(b)
			except KeyError:
				adj_list[a] = set([b])

		return adj_list

	# based on http://www.fit.vutbr.cz/study/courses/GAL/public/gal-slides.pdf
	@staticmethod
	def transposeGraph(graph):
		nodes = graph.nodes()
		edges = graph.edges()
		tedges = {}
		for u in edges:
			for v in edges[u]:
				# (u,v) -> (v,u)
				if v not in tedges:
					tedges[v] = set([u])
				else:
					tedges[v].add(u)

		return Graph(nodes, tedges)

	@staticmethod
	def getLeafNodes(graph):
		nodes = graph.nodes()
		edges = graph.edges()

		leaves = set([])

		for u in nodes:
			# u has no edges or edges[u] is empty
			if u not in edges or edges[u] == []:
				leaves.add(u)

		return leaves

	@staticmethod
	def getRootNodes(graph):
		nodes = graph.nodes()
		edges = graph.edges()

		visited = {}
		for u in nodes:
			visited[u] = 0

		for u in nodes:
			if u in edges:
				for v in edges[u]:
					visited[v] = 1

		roots = set([])
		for u in nodes:
			if visited[u] == 0:
				roots.add(u)

		return roots

	@staticmethod
	def joinGraphs(g1, g2):
		nodes = g1.nodes()
		edges = g1.edges()
		g2_edges = g2.edges()

		for u in g2.nodes():
			if u not in nodes:
				nodes.add(u)

			if u not in g2_edges:
				continue

			for v in g2_edges[u]:
				if u in edges:
					if v in edges[u]:
						continue
					edges[u].add(v)
				else:
					edges[u] = set([v])

		return Graph(nodes, edges)

	@staticmethod
	def getSCCs(graph):
		return SCCBuilder(graph).build().getSCC()

	@staticmethod	
	def getReacheableSubgraph(graph, node):
		nodes = graph.nodes()
		edges = graph.edges()
		dfs = DFS(graph)
		reacheable = dfs.DFSSimpleWalk(node)

		r_edges = {}
		for u in reacheable:
			if u not in edges:
				continue

			r_edges[u] = set([])
			for v in edges[u]:
				if v in reacheable:
					r_edges[u].add(v)

		return Graph(reacheable, r_edges)

	@staticmethod
	def truncateGraph(graph, root_nodes):
		"""Create a set of all nodes containg the root_nodes and
		   all nodes reacheable from them
		"""
		subgraph = Graph()
		for node in root_nodes:
			subgraph = GraphUtils.joinGraphs(subgraph, GraphUtils.getReacheableSubgraph(graph, node))

		return subgraph

	@staticmethod
	def filterGraph(graph, node_fnc):
		"""Remove all nodes for with node_fnc does not hold
		"""
		nodes = filter(lambda l: node_fnc(l), graph.nodes())
		edges = {}

		gedges = graph.edges()
		for u in gedges:
			if u not in nodes:
				continue
			for v in gedges[u]:
				if v not in nodes:
					continue
				try:
					edges[u].append(v)
				except KeyError:
					edges[u] = [v]

		return Graph(nodes, edges)

class SCCBuilder(object):

	def __init__(self, graph):
		self._graph = graph
		self._sccs = set([])

	def getSCC(self):
		return self._sccs

	def build(self):
		nodes = self._graph.nodes()
		edges = self._graph.edges()
		f, d = DFS(self._graph).DFSWalk()
		tgraph = GraphUtils.transposeGraph(self._graph)
		start_nodes, pred = DFS(tgraph).DFSWalk(f)
		trees = []
		for node in start_nodes:
			trees.append(self._getSucc(node, pred))
	
		# some trees can overlap
		sccs = []
		for i_tree in trees:
			# iss = is subset
			iss = False
			for j_tree in trees:
				if i_tree == j_tree:
					continue
				if set(i_tree).issubset(j_tree):
					iss = True
			if iss == False:
				# if the scc has one node and there is no edge
				# skip it
				if len(i_tree) == 1:
					if i_tree[0] not in edges:
						continue
					if i_tree[0] not in edges[i_tree[0]]:
						continue

				sccs.append(frozenset(i_tree))
	
		self._sccs = set(sccs)

		return self

	@staticmethod
	def _getSucc(s, pred):
		if pred[s] == '':
			return [s]
		else:
			return [s] + SCCBuilder._getSucc(pred[s], pred)

class DFS:

	def __init__(self, graph):
		self.nodes = graph.nodes()
		self.edges = graph.edges()

		self.WHITE=0
		self.GRAY=1
		self.BLACK=2

		self.color = {}
		self.d = {}
		self.f = {}
		self.time = 0
		self.pred = {}

	def DFSVisit(self, node):
		self.color[node] = self.GRAY
		self.time += 1
		self.d[node] = self.time

		if node in self.edges:
			for adj in self.edges[node]:
				if self.color[adj] == self.WHITE:
					self.pred[adj] = node
					self.DFSVisit(adj)

		self.color[node] = self.BLACK
		self.time += 1
		self.f[node] = self.time

	def DFSSimpleWalk(self, start_node):
		for node in self.nodes:
			self.color[node] = self.WHITE
			self.pred[node] = ""

		self.time = 0
		self.DFSVisit(start_node)

		reachable = set([])
		for node in self.nodes:
			if self.color[node] != self.WHITE:
				reachable.add(node)

		return reachable

	def DFSWalk(self, f = []):
		for node in self.nodes:
			self.color[node] = self.WHITE
			self.pred[node] = ""

		self.time = 0

		if f == []:
			for node in self.nodes:
				if self.color[node] == self.WHITE:
					self.DFSVisit(node)
			return (self.f, self.d)
		else:
			start_nodes = []
			for node, _ in sorted(f.items(), key=operator.itemgetter(1), reverse=True):
				if self.color[node] == self.WHITE:
					self.DFSVisit(node)
				start_nodes.append(node)

			return (start_nodes, self.pred)





