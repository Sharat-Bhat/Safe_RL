class SafetyRules:
	#First List : Time Step
	#Second List : Disjunction
	#Third List : Conjunction
	dict_safety_rules = {
			"sp-1":((("water"))),
			"sp-2":((("water")),(("water"))),
			"sp-3":((("water")),(("water")),(("water"))),
			"sp-4":((("water")),(("water")),(("water")),(("water"))),
			"sp-5":((("water")),(("water")),(("water")),(("water")),(("water")))
		}
	def __init__(self, safety_rule_id="sp-3", unsafe_penalty=0):
		self.safety_rule_id = safety_rule_id
		self.safety_prop = self.dict_safety_rules[self.safety_rule_id]
		self.safety_prop_time_length = len(self.safety_prop)
		self.unsafe_penalty = unsafe_penalty
	
	def check_safety(self, history):
		safety_flag = True
		for i in range(0, self.safety_prop_time_length): #Time Step
			safety_prop_time = self.safety_prop[i]
			if len(history)<self.safety_prop_time_length:
				safety_flag = False
				break
			history_time = history[-1*(self.safety_prop_time_length-i)]
			safety_time_or_flag = False
			for j in range(0, len(safety_prop_time)): #Disjunction
				safety_prop_time_or = safety_prop_time[j]
				safety_time_or_and_flag = True
				for k in range(0, len(self.safety_prop[i][j])): #Conjuction
					safety_prop_time_or_and = safety_prop_time_or[k]
					if safety_prop_time_or_and == history_time:
						continue
					else:
						safety_time_or_and_flag = False
						break
				if safety_time_or_and_flag:
					safety_time_or_flag = True
			if safety_time_or_flag == False:
				safety_flag = False
				break
		return safety_flag

	def set_unsafe_penalty(self, unsafe_penalty):
		self.unsafe_penalty = unsafe_penalty	



	def SPtoGraph(self):
		dict_graph = {}
		graph = []

		lst_vertices = []		
		for i in range(0, len(self.safety_prop)+1):
			lst_vertices.append(i)

		lst_labels = [(("water")), (("not_water"))]

		for i in range(0, len(lst_vertices)):
			row = []
			for j in range(0, len(lst_labels)):
				row.append([])
			graph.append(row)
		
		for i in range(0, len(lst_vertices)):
			vertex = lst_vertices[i]
			row = graph[i]
			for j in range(0, len(lst_labels)):
				label = lst_labels[j]
				next_vertices = []
				next_vertices_weights = []
				next_vertex = 0
				if vertex == len(self.safety_prop):
					next_vertex = vertex
				else:				
					if label == self.safety_prop[vertex]:
						next_vertex = vertex + 1	
				
				next_vertex_indx = lst_vertices[next_vertex]

				next_vertices.append(next_vertex_indx)
				next_vertices_weights.append(1.0)
				row[j] = [next_vertices, next_vertices_weights]
			graph[i] = row

		dict_graph["graph"] = graph
		dict_graph["vertices"] = lst_vertices
		dict_graph["labels"] = lst_labels
		self.SP_Graph = dict_graph

		print("dict_SP_graph")
		#print(dict_graph)

		return dict_graph


	def get_cross_graph(self, graph1, graph2):
		dict_cross_graph = {}
		cross_graph = []
		lst_vertices = []
		lst_labels = []

		for vertex1 in graph1["vertices"]:
			for vertex2 in graph2["vertices"]:
				lst_vertices.append(tuple([vertex1, vertex2]))
			
		for label1 in graph1["labels"]:
			for label2 in graph2["labels"]:
				lst_labels.append(tuple([label1, label2]))

		for _ in lst_vertices:
			row = []
			for _ in lst_labels:
				row.append([])
			cross_graph.append(row)

		for i in range(0, len(lst_vertices)):
			vertex = lst_vertices[i]
			vertex1 = vertex[0]
			vertex2 = vertex[1]

			vertex1_indx = graph1["vertices"].index(vertex1)
			vertex2_indx = graph2["vertices"].index(vertex2)
			row = cross_graph[i]
			for j in range(0, len(lst_labels)):
				label = lst_labels[j]
				label1 = label[0]
				label2 = label[1]

				label1_indx = graph1["labels"].index(label1)
				label2_indx = graph2["labels"].index(label2)

				dest_vertex1_indices = graph1["graph"][vertex1_indx][label1_indx][0]
				dest_vertex1_weights = graph1["graph"][vertex1_indx][label1_indx][1]

				dest_vertex2_indices = graph2["graph"][vertex2_indx][label2_indx][0]
				dest_vertex2_weights = graph2["graph"][vertex2_indx][label2_indx][1]

				dest_vertex_indices = []
				dest_vertex_weights = []
				for k, v1 in enumerate(dest_vertex1_indices):
					for l, v2 in enumerate(dest_vertex2_indices):
						dest_vertex_indx = lst_vertices.index(tuple([graph1["vertices"][v1], graph2["vertices"][v2]]))
						dest_vertex_indices.append(dest_vertex_indx)
						dest_vertex_weights.append(dest_vertex1_weights[k]*dest_vertex2_weights[l])
				row[j] = [dest_vertex_indices, dest_vertex_weights]
			
			cross_graph[i] = row
				
		
		dict_cross_graph["graph"] = cross_graph
		dict_cross_graph["vertices"] = lst_vertices
		dict_cross_graph["labels"] = lst_labels
		
		print("dict_cross_graph")
		print(dict_cross_graph)

		return dict_cross_graph


