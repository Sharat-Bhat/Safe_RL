import numpy as np

HORIZON=10
LOOK_AHEAD=10
GAMMA=0.5
NUM_ACTIONS=4
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
transition_prob=[0.75, 0.1, 0.1, 0.05]

layout_dir = "layouts/"
layout_name = "smallClassic.lay"
layout_path = layout_dir+layout_name

pacmans = []
ghosts = []

def getLayout(layout_path):
    with open(layout_path) as f:
        lines = f.readlines()
    lines = [list(line.strip()) for line in lines]
    lines = np.array(lines)
    return lines

def getPacman(layout):
    pm = np.where(layout=='P')
    return np.array(pm).T

def getGhost(layout):
    ghosts = np.where(layout=='G')
    return np.array(ghosts).T

def initMap(layout):
    prob_map = np.zeros(layout.shape)
    prob_map += np.ones(layout.shape)*(layout=='G')
    return prob_map

def getVisibilityMap(layout, pacmans, horizon=HORIZON):
    visible = np.zeros(layout.shape)
    min_depth = (layout!='%')+0.0
    min_depth[min_depth == 1] = np.inf
    print(min_depth)
    st = []
    pacmans = pacmans.tolist()
    for pacman in pacmans:
        node = pacman
        node.append(0)
        min_depth[node[0],node[1]] = 1
        st.append(node)
        while len(st) > 0:
            top = st[-1]
            if top[2] < horizon:
                if top[0] > 0 and min_depth[top[0]-1][top[1]] > min_depth[top[0]][top[1]]+1:
                    min_depth[top[0]-1, top[1]] = min_depth[top[0]][top[1]]+1
                    node = [top[0]-1, top[1], top[2]+1]
                    st.append(node)
                elif top[1] > 0 and min_depth[top[0]][top[1]-1] > min_depth[top[0]][top[1]]+1:
                    min_depth[top[0], top[1]-1] = min_depth[top[0]][top[1]]+1
                    node = [top[0], top[1]-1, top[2]+1]
                    st.append(node)
                elif top[0] < layout.shape[0]-1 and min_depth[top[0]+1][top[1]] > min_depth[top[0]][top[1]]+1:
                    min_depth[top[0]+1, top[1]] = min_depth[top[0]][top[1]]+1
                    node = [top[0]+1, top[1], top[2]+1]
                    st.append(node)
                elif top[1] < layout.shape[1]-1 and min_depth[top[0]][top[1]+1] > min_depth[top[0]][top[1]]+1:
                    min_depth[top[0], top[1]+1] = min_depth[top[0]][top[1]]+1
                    node = [top[0], top[1]+1, top[2]+1]
                    st.append(node)
                else:
                    visible[top[0], top[1]] = 1
                    st.pop()
            else:
                visible[top[0], top[1]] = 1
                st.pop()
    final_visibility = layout
    final_visibility[visible!=1] = '?'
    return final_visibility

def getSafetyMap(visibility_map, look_ahead=LOOK_AHEAD):
    safety_map =np.zeros(visibility_map.shape)
    safety_map[visibility_map=='?'] = -1
    safety_map[visibility_map=='G'] = 1
    ghosts = np.array(np.where(visibility_map=='G')).T.tolist()
    ghosts = [tuple(ghost) for ghost in ghosts]
    min_depth = (visibility_map!='?')+0.0
    min_depth[min_depth == 1] = np.inf
    ghost_set =np.zeros(visibility_map.shape)
    pacman_set =np.zeros(visibility_map.shape)
    pacman_set[visibility_map=='P'] = 1
    print("Pacman set:")
    print(pacman_set)
    pacmans = np.array(np.where(visibility_map=='P')).T.tolist()
    pacmans = [tuple(pacman) for pacman in pacmans]
    for ghost in ghosts:
        ghost_set[ghost[0]][ghost[1]] = 1
        
    for i in range(look_ahead+1):
        prev_ghost_set = ghost_set
        ghost_set = np.zeros(visibility_map.shape)
        prev_pacman_set = pacman_set
        pacman_set = np.zeros(pacman_set.shape)
        prev_ghosts = list(set(ghosts))
        ghosts=[]
        for ghost in prev_ghosts:
            if ghost[0]>0 and visibility_map[ghost[0]-1][ghost[1]] != '?':
                ghost_set[ghost[0]-1][ghost[1]] = 1
                ghosts.append((ghost[0]-1, ghost[1]))
            if ghost[1]>0 and visibility_map[ghost[0]][ghost[1]-1] != '?':
                ghost_set[ghost[0]][ghost[1]-1] = 1
                ghosts.append((ghost[0], ghost[1]-1))
            if ghost[0]<ghost_set.shape[0]-1 and visibility_map[ghost[0]+1][ghost[1]] != '?':
                ghost_set[ghost[0]+1][ghost[1]] = 1
                ghosts.append((ghost[0]+1, ghost[1]))
            if ghost[1]<ghost_set.shape[1]-1 and visibility_map[ghost[0]][ghost[1]+1] != '?':
                ghost_set[ghost[0]][ghost[1]+1] = 1
                ghosts.append((ghost[0], ghost[1]+1))
        prev_pacmans=list(set(pacmans))
        pacmans=[]
        # print(ghost_set)
        safety_map =np.zeros((visibility_map.shape[0], visibility_map.shape[1], NUM_ACTIONS))
        for pacman in prev_pacmans:
            x = pacman[0]
            y = pacman[1]
            for action in ACTIONS:
                # prev_pacman_set = prev_pacman_set
                if action == "UP":
                    if x > 0 and visibility_map[x-1][y] != '%' and visibility_map[x-1][y] != '?': 
                        pacman_set[x-1][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][0] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x-1][y]
                        pacmans.append((x-1, y))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][0] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if y > 0 and visibility_map[x][y-1] != '%' and visibility_map[x][y-1] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y-1]
                        pacmans.append((x, y-1))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][1] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if x < visibility_map.shape[0]-1 and visibility_map[x+1][y] != '%' and visibility_map[x+1][y] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x+1][y]
                        pacmans.append((x+1, y))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][3] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if y < visibility_map.shape[1]-1 and visibility_map[x][y+1] != '%' and visibility_map[x][y+1] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y+1]
                        pacmans.append((x, y+1))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][2] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                
                elif action == "DOWN":
                    if x > 0 and visibility_map[x-1][y] != '%' and visibility_map[x-1][y] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x-1][y]
                        pacmans.append((x-1, y))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][3] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if y > 0 and visibility_map[x][y-1] != '%' and visibility_map[x][y-1] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y-1]
                        pacmans.append((x, y-1))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][2] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if x < visibility_map.shape[0]-1 and visibility_map[x+1][y] != '%' and visibility_map[x+1][y] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x+1][y]
                        pacmans.append((x+1, y))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][0] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if y < visibility_map.shape[1]-1 and visibility_map[x][y+1] != '%' and visibility_map[x][y+1] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y+1]
                        pacmans.append((x, y+1))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][1] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                
                elif action == "LEFT":
                    if x > 0 and visibility_map[x-1][y] != '%' and visibility_map[x-1][y] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x-1][y]
                        pacmans.append((x-1, y))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][2] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if y > 0 and visibility_map[x][y-1] != '%' and visibility_map[x][y-1] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y-1]
                        pacmans.append((x, y-1))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][0] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if x < visibility_map.shape[0]-1 and visibility_map[x+1][y] != '%' and visibility_map[x+1][y] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x+1][y]
                        pacmans.append((x+1, y))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][1] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if y < visibility_map.shape[1]-1 and visibility_map[x][y+1] != '%' and visibility_map[x][y+1] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y+1]
                        pacmans.append((x, y+1))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][3] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
        
                elif action == "RIGHT":
                    if x > 0 and visibility_map[x-1][y] != '%' and visibility_map[x-1][y] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x-1][y]
                        pacmans.append((x-1, y))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][1] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if y > 0 and visibility_map[x][y-1] != '%' and visibility_map[x][y-1] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y-1]
                        pacmans.append((x, y-1))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][3] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if x < visibility_map.shape[0]-1 and visibility_map[x+1][y] != '%' and visibility_map[x+1][y] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x+1][y]
                        pacmans.append((x+1, y))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][2] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
                    if y < visibility_map.shape[1]-1 and visibility_map[x][y+1] != '%' and visibility_map[x][y+1] != '?': 
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y+1]
                        pacmans.append((x, y+1))
                    else:
                        # pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacman_set[x][y] += prev_pacman_set[x][y]*transition_prob[0]
                        safety_map[x][y][0] += prev_pacman_set[x][y]*transition_prob[0]*ghost_set[x][y]
                        pacmans.append((x, y))
        # print(pacman_set)
        print(pacman_set)
    return safety_map
        

def main():
    layout = getLayout(layout_path=layout_path)
    print(getLayout(layout_path=layout_path))
    pacmans = getPacman(layout=layout)
    print(pacmans)
    ghosts = getGhost(layout=layout)
    print(ghosts)
    prob_map = initMap(layout=layout)
    print(prob_map)
    visibility_map = getVisibilityMap(layout=layout, pacmans=pacmans)
    print(visibility_map)
    safety_map = getSafetyMap(visibility_map=visibility_map)
    print(safety_map)

if __name__=="__main__":
    main()