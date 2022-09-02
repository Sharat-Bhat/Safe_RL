import random

PATH = "layout/openClassic.lay"
# PATH = "layout/mediumClassic.lay"
# PATH = "layout/testSmall.lay"

def get_layout(path):
    layout = []
    file1 = open(path)
    layout = file1.read()
    layout = layout.split('\n')
    layout = list(filter(None, layout))
    print(layout)
    return layout

class Game:
    def __init__(self, grid):
        self.grid = grid
        self.ghosts = []
        self.pacman = None
        self.height = len(grid)
        self.width = len(grid[0])
        # HALT=0, LEFT=(0,-1), RIGHT=(0,1), UP=(-1,0), DOWN=(1,0)
        self.actions = [(0,0), (0,-1), (0,1), (-1,0), (1,0)]
        self.num_actions = len(self.actions)
        print(self.height, self.width)
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == 'P':
                    print(i,j)
                    self.pacman = (i,j)
                elif self.grid[i][j] == 'G':
                    print(i,j)
                    self.ghosts.append((i,j))
        self.num_ghosts = len(self.ghosts)
        self.graph = []
        self.graph_size = (self.height*self.width)**(self.num_ghosts+1)
        temp = []
        # for i in range(self.num_actions):
        #     newdict = dict()
        #     temp.append(newdict)
        self.graph = []
        for i in range(self.graph_size+1):
            newlist = list()
            for j in range(self.num_actions):
                newdict = dict()
                newlist.append(newdict)
            self.graph.append(newlist)
            # self.graph.append(newlist)# = [temp]*(self.graph_size+1)
        # self.graph = [[{}]*self.num_actions]*(self.graph_size+1)
        self.state = self.coordinates_to_states(self.pacman, self.ghosts)
        print(self.state, self.pacman, self.ghosts)

        
    def state_to_coordinates(self, state):
        size = self.width*self.height
        g = []
        for i in range(self.num_ghosts):
            g0 = state%size
            state = int((state-g0)/size)
            g0 = (int(g0/self.width), int(g0%self.width))
            g.insert(0, g0)

        p = state
        p = (int(p/self.width), int(p%self.width))
        # print (p, g1, g2)
        return p, g
        
    def coordinates_to_states(self, p, g):
        size = self.width*self.height
        state=0
        state += self.width*p[0] + p[1]
        for i in range(len(g)):
            state *= size
            state += self.width*g[i][0] + g[i][1]
        return state

    def play(self, num_iter=1000):
        default = self.state
        for i in range(num_iter):
            self.state = default
            
            # print("Iteration = ", i)
            num = 10000
            for j in range(num):
                action = random.randint(0,self.num_actions-1)
                curr_state = self.state
                p, g = self.state_to_coordinates(curr_state)
                p_next = tuple([sum(x) for x in zip(p, self.actions[action])])
                ag = []
                g_next = []
                # print(p,g)
                for k in range(self.num_ghosts):
                    ag.append(random.randint(0,self.num_actions-1))
                    g_next.append(tuple([sum(x) for x in zip(g[k], self.actions[ag[k]])]))
                if self.grid[p_next[0]][p_next[1]] != '%':
                    p = p_next
                    temp = -1
                    for k in range(self.num_ghosts):
                        if p == g[k]:
                            # print(p, g[k])
                            next_state = self.coordinates_to_states(p, g)
                            self.graph[curr_state][action][next_state] = self.graph[curr_state][action].get(next_state, 0) + 1
                            temp=k
                            break
                    if temp > -1:
                        break
                for k in range(self.num_ghosts):
                    if self.grid[g_next[k][0]][g_next[k][1]] != '%':
                        g[k] = g_next[k]
                # print(p,g)
                
                next_state = self.coordinates_to_states(p, g)
                
                self.graph[curr_state][action][next_state] = self.graph[curr_state][action].get(next_state, 0) + 1
                self.state = next_state
                for k in range(self.num_ghosts):
                    temp = -1
                    if p == g[k]:
                        temp=k
                        break
                if temp > -1:
                    break
            # print(self.graph[261][3])
            # print(self.graph[260][3])
            # print()
        for i in range(self.graph_size):
            for j in range(self.num_actions):
                self.graph[i][j] = {k: v / total for total in (sum(self.graph[i][j].values()),) for k, v in self.graph[i][j].items()}
                if self.graph[i][j]:
                    print("\n", i, j, self.graph[i][j])
        # print(self.graph)
                
            
grid = get_layout(PATH)
game = Game(grid)
game.play(num_iter=10000)