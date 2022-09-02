import random as rd
from colorama import Fore, Back, Style
from SafetyRules import SafetyRules

class Environment:
	B = "boundary"
	W = "water"
	L = "land"

	state_types = {"boundary":B, "water": W, "land": L}

	GW_Map_1 = [
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]
		]

	GW_Map_2 = [
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]
		]

	GW_Map_3 = [
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]
		]

	GW_Map_4 = [
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]
		]

	GW_Map_5 = [
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, L, B, B, B, B],
		[B, L, L, L, L, L, L, L, B, W, B, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, L, B, B, B, B, B, B, W, B, B, B, B, B, B, B, B, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, W, B, B, B, B, B, B, B, L, B, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, L, L, L, L, L, L, L, L, W, L, L, L, L, L, L, L, L, L, B],
		[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]
		]

	dict_environments = {
		"Map-1": GW_Map_1,
		"Map-2": GW_Map_2,
		"Map-3": GW_Map_3,
		"Map-4": GW_Map_4,
		"Map-5": GW_Map_5
	}

	action_list = ["Up", "Right", "Down", "Left",]

	def __init__(self, map_id="Map-1", safety_rule="sp-3", unsafe_penalty=0, ndt_flag=False, ndt_prob=0.0, start_pos=(0,0), seed=0):
		self.map_id = map_id
		self.env = self.dict_environments[map_id]
		self.sp_id = safety_rule
		self.sp = SafetyRules(safety_rule, unsafe_penalty)
		self.env_size = (len(self.env), len(self.env[0]))
		self.ndt_flag = ndt_flag
		self.ndt_prob = ndt_prob
		self.curr_state = start_pos
		self.state_reward = {}
		self.state_history = []
		self.state_history.append(self.curr_state)
		rd.seed(seed)

	def set_start_state(self, start_pos):
		self.start_state = start_pos
		self.reset()
	
	def set_goal_state(self, goal_pos):
		self.goal_state = goal_pos

	def get_state_reward(self, state_pos):
		state_reward = 0.0
		if state_pos in self.state_reward.keys():
			state_reward = self.state_reward[state_pos]
		return state_reward

	def set_state_reward(self, state_pos, state_reward):
		self.state_reward[state_pos] = state_reward

	def reset(self):
		self.curr_state = self.start_state
		self.state_history = []
		self.state_history.append(self.get_state_type(self.curr_state))

	def get_state_type(self, cell_pos):
		return self.env[cell_pos[0]][cell_pos[1]]

	def get_action_list(self):
		return self.action_list

	def set_action_list(self, action_list):
		self.action_list = action_list

	def step(self, action):
		next_state = self.curr_state
		reward = 0.0
		done = False
		info = {}
		
		lst_next_states_and_weights = self.get_weighted_next_states(self.curr_state, action)
		
		next_state = rd.choices(lst_next_states_and_weights[0], weights=lst_next_states_and_weights[1])
		
		if next_state == self.goal_state:
			done = True
			print(self.get_state_reward(next_state))
			#input()
		
		reward = self.get_state_reward(next_state)
		self.curr_state = next_state
		self.state_history.append(self.get_state_type(self.curr_state))

		safety_flag = self.sp.check_safety(self.state_history)
		if safety_flag:
			reward = self.sp.unsafe_penalty
			done = True
		
		info["safety_flag"] = safety_flag

		return next_state, reward, done, info

	def print(self, q_table=None):
		print(Fore.BLACK + Back.BLACK + "                                                                       ", end="")
		print(Style.RESET_ALL, end="")
		print()
		for i in range(0, self.env_size[0]):
			print(Fore.BLACK + Back.BLACK + " ", end="")
			print(Style.RESET_ALL, end="")
			for j in range(0, self.env_size[1]):
				if q_table == None:
					max_q_val = 0.00
					max_q_val_action_code = "X"
				else:
					max_q_val = max(q_table[i][j])
					max_q_val_action_code = self.action_list[q_table[i][j].index(max_q_val)][0]

				color_style = ""
				if self.env[i][j] == "boundary":
					color_style = Fore.WHITE + Back.RED
				elif self.env[i][j] == "water":
					color_style = Fore.WHITE + Back.BLUE
				elif self.env[i][j] == "land":
					color_style = Fore.BLACK + Back.WHITE
				elif self.goal_state == (i,j):
					color_style = Fore.WHITE + Back.GREEN
				elif self.start_state == (i,j):
					color_style = Fore.WHITE + Back.YELLOW
					

				if self.env[i][j] == "boundary":
					print(color_style + "         ", end="")
				else:
					if max_q_val < 0:
						print(color_style + "-%06.2f %s" % (round(abs(max_q_val), 2), max_q_val_action_code), end="")
					else:
						print(color_style + "+%06.2f %s" % (round(abs(max_q_val), 2), max_q_val_action_code), end="")
				print(Style.RESET_ALL, end="")
				print(Fore.BLACK + Back.BLACK + " ", end="")
				print(Style.RESET_ALL, end="")

			print()	
			print(Fore.BLACK + Back.BLACK + "                                                                       ", end="")
			print(Style.RESET_ALL, end="")
			print()


	def get_weighted_next_states(self, state, action):
		lst_next_states_and_weights = []
		next_state = state
		if self.ndt_flag == False:
			if(action == "Up"):
				next_state = (state[0]-1, state[1])
			elif(action == "Down"):
				next_state = (state[0]+1, state[1])
			elif(action == "Left"):
				next_state = (state[0], state[1]-1)
			elif(action == "Right"):
				next_state = (state[0], state[1]+1)
			
			if self.get_state_type(next_state) == "boundary":
				next_state = state

			lst_next_states_and_weights.append([next_state])
			lst_next_states_and_weights.append([1.0])
		else:
			lst_next_state_probs = []
			lst_next_states = []

			ndt_action = action
			lst_next_state_probs.append(1.0-self.ndt_prob)
			if(ndt_action == "Up"):
				next_state = (state[0]-1, state[1])
			elif(ndt_action == "Down"):
				next_state = (state[0]+1, state[1])
			elif(ndt_action == "Left"):
				next_state = (state[0], state[1]-1)
			elif(ndt_action == "Right"):
				next_state = (state[0], state[1]+1)

			if self.get_state_type(next_state) == "boundary":
				next_state = state

			lst_next_states.append(next_state)

			#Left side action
			action_index = self.action_list.index(action)
			action_index = (action_index + len(self.action_list) - 1)%len(self.action_list)
			ndt_action = self.action_list[action_index]
			lst_next_state_probs.append(self.ndt_prob/2.0)
			if(ndt_action == "Up"):
				next_state = (state[0]-1, state[1])
			elif(ndt_action == "Down"):
				next_state = (state[0]+1, state[1])
			elif(ndt_action == "Left"):
				next_state = (state[0], state[1]-1)
			elif(ndt_action == "Right"):
				next_state = (state[0], state[1]+1)

			if self.get_state_type(next_state) == "boundary":
				next_state = state

			lst_next_states.append(next_state)

			#Right side action
			action_index = self.action_list.index(action)
			action_index = (action_index + len(self.action_list) + 1)%len(self.action_list)
			ndt_action = self.action_list[action_index]
			lst_next_state_probs.append(self.ndt_prob/2.0)
			if(ndt_action == "Up"):
				next_state = (state[0]-1, state[1])
			elif(ndt_action == "Down"):
				next_state = (state[0]+1, state[1])
			elif(ndt_action == "Left"):
				next_state = (state[0], state[1]-1)
			elif(ndt_action == "Right"):
				next_state = (state[0], state[1]+1)
			
			if self.get_state_type(next_state) == "boundary":
				next_state = state
			lst_next_states.append(next_state)
			
			lst_next_states_and_weights.append(lst_next_states)
			lst_next_states_and_weights.append(lst_next_state_probs)
		
		#print(state, lst_next_states_and_weights)

		return lst_next_states_and_weights


	#Incidence Graph : States are Nodes and Action are Edges or Edge Label
	def MDPtoGraph(self):
		dict_graph = {}
		graph = []
		lst_labels = self.action_list
		lst_vertices = []
		for i in range(self.env_size[0]):
			for j in range(self.env_size[1]):
				if self.env[i][j] in ["water", "land"]:
					lst_vertices.append((i,j))
		
		
		for vertex in lst_vertices:
			row = []
			for label in lst_labels:
				row.append([])
			graph.append(row)
		
		
		
		for i in range(0, len(lst_vertices)):
			vertex = lst_vertices[i]
			row = graph[i]
			for j in range(0, len(lst_labels)):
				label = lst_labels[j]
				next_weighted_vertices = self.get_weighted_next_states(vertex, label)

				#print(vertex)
				lst_next_vertices = next_weighted_vertices[0]
				lst_next_weights = next_weighted_vertices[1]

				lst_next_vertices_indx = []
				for v in lst_next_vertices:
					v_index = lst_vertices.index(v)
					lst_next_vertices_indx.append(v_index)
				row[j] = [lst_next_vertices_indx, lst_next_weights]
			graph[i] = row


		dict_graph["graph"] = graph
		dict_graph["vertices"] = lst_vertices
		dict_graph["labels"] = lst_labels
		self.MDP_Graph = dict_graph

		print("dict_MDP_graph")
		#print(dict_graph)

		return dict_graph