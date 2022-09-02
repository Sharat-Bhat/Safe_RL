import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image as im

LOOK_AHEAD=5
HORIZON = 2*LOOK_AHEAD
GAMMA=0.5
NUM_ACTIONS=5
ACTIONS = ["North", "West", "East", "South", "Stop"]
DIRECTIONS = ["North", "West", "East", "South", "Stop"]

transition_prob={"North": [1,0,0,0,0],
                 "West": [0,1,0,0,0],
                 "East": [0,0,1,0,0],
                 "South": [0,0,0,1,0],
                 "Stop": [0,0,0,0,1]
                 }
# transition_prob={"North": [.96,0.02,0.02,0],
#                  "West": [0.02,.96,0,0.02],
#                  "East": [0.02,0,.96,0.02],
#                  "South": [0,0.02,0.02,.96]
#                  }

# transition_prob={"North": [0.75, 0.1, 0.1, 0.05],
#                  "West": [0.1, 0.75, 0.05, 0.1],
#                  "East": [0.1, 0.05, 0.75, 0.1],
#                  "South": [0.05, 0.1, 0.1, 0.75]
#                  }
# transition_prob={"North": [.6,0.2,0.2,0],
#                  "West": [0.2,.6,0,0.2],
#                  "East": [0.2,0,.6,0.2],
#                  "South": [0,0.2,0.2,.6]
#                  }

layout_dir = "layouts/"
layout_name = "originalClassic.lay"
layout_name = "smallClassic.lay"
layout_name = "test.lay"
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
    print(pm)
    return np.array(pm).T

def getGhost(layout):
    ghosts = np.where(layout=='G')
    return np.array(ghosts).T

def initMap(layout):
    prob_map = np.zeros(layout.shape)
    # prob_map += np.logical_and(np.ones(layout.shape),(layout=='G'))
    prob_map[layout=='G'] = 1
    prob_map = prob_map
    return prob_map

def getVisibilityMap(layout, pacmans, horizon=HORIZON):
    visible = np.zeros(layout.shape)
    min_depth = (layout!='%')+0.0
    min_depth[min_depth == 1] = np.inf
    # print(min_depth)
    st = []
    pacmans = pacmans.tolist()
    for pacman in pacmans:
        node = pacman
        node.append(0)
        min_depth[node[0],node[1]] = 0
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
    
    for ghost in ghosts:
        ghost_set[ghost[0]][ghost[1]] = 1
    
    ghost_maps = []
    ghost_maps.append(ghost_set)
    ghost_maps.append(ghost_set)
    plt.imshow(ghost_set)
    plt.colorbar()
    plt.show()
    for i in range(look_ahead+1):
        prev_ghost_set = ghost_set
        ghost_set = np.zeros(visibility_map.shape)
        prev_ghosts = list(set(ghosts))
        ghosts=[]
        for ghost in prev_ghosts:
            ghosts.append(ghost)
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
        ghost_maps.append(ghost_set)
        plt.imshow(ghost_set)
        plt.colorbar()
        plt.show()

    pacman_maps = np.zeros((look_ahead+1, visibility_map.shape[0], visibility_map.shape[1])      )  
    action_prob_map = []
    final_action_map = []
    pacman_maps[look_ahead] = ghost_maps[look_ahead]
    level = look_ahead-1
    while level >=0:
        cells = np.array(np.where(visibility_map!='?')).T.tolist()
        pacman_safety_map = np.ones(visibility_map.shape)
        action_prob = {}
        # final_action = np.copy(visibility_map)
        for action in ACTIONS:
            action_safety_map = np.zeros(visibility_map.shape)
            for i in range(len(transition_prob[action])):

                temp = np.zeros(visibility_map.shape)
                if i==0:
                    dist = 1
                    axis = 0
                elif i==1:
                    dist = 1
                    axis = 1
                elif i==2:
                    dist = -1
                    axis = 1
                elif i==3:
                    dist = -1
                    axis = 0
                else:
                    dist=0
                    axis=0
                vis_shift = np.roll(visibility_map, dist, axis=axis)
                pacman_shift = np.roll(pacman_maps[level+1], dist,axis=axis)
                b_check = np.ones(visibility_map.shape)
                b_check[0][:] = 0
                # print(b_check.shape)
                # print(vis_shift.shape)
                # print(visibility_map.shape)
                mask = np.logical_and(np.array(vis_shift != '%'), np.array(vis_shift != '?'))
                # mask = np.logical_and(mask, b_check)
                # print(mask)
                # print(transition_prob[action][i])
                # print(pacman_shift.shape)
                temp = transition_prob[action][i]*(pacman_shift*(mask == True) + pacman_maps[level+1]*(mask==False))
                # action_safety_map = np.maximum(action_safety_map, temp)
                action_safety_map += temp
                action_safety_map[visibility_map == '?'] = 1
                action_safety_map[ghost_maps[level] == 1] = 1
                
            pacman_safety_map = np.minimum(action_safety_map, pacman_safety_map)
            # final_action[pacman_safety_map==action_safety_map] = action[0]
            action_prob[action] = action_safety_map
        # final_action[visibility_map == '?'] = '?'
        # print("Final Action: ")
        # print(final_action)
        action_prob_map.insert(0, action_prob)     
        # final_action_map.insert(0, final_action)
        pacman_safety_map[ghost_maps[level] == 1] = 1
        # pacman_safety_map[visibility_map == '%'] = 4
        pacman_safety_map[visibility_map == '?'] = 1
        pacman_maps[level] = pacman_safety_map  
        # for i  in range(LOOK_AHEAD+1):
        plt.imshow(pacman_safety_map)
        plt.colorbar()
        plt.tight_layout()
        plt.grid(linewidth=1)        
        plt.show()                       
        level -= 1
    
    # for i in range(LOOK_AHEAD+1):
    #     plt.imshow(final_action_map[i])
    #     plt.colorbar()
    #     plt.show()
    safety_map = pacman_maps[0]
    action_map = action_prob_map[0]        
    return safety_map, action_map

def getSafeActions(visibility_map, legalActions, look_ahead=0):
        safety_map =np.zeros(visibility_map.shape)
        safety_map[visibility_map=='?'] = -1
        safety_map[visibility_map=='G'] = 1
        ghosts = np.array(np.where(visibility_map=='G')).T.tolist()
        ghosts = [tuple(ghost) for ghost in ghosts]
        # min_depth = (visibility_map!='?')+0.0
        # min_depth[min_depth == 1] = np.inf
        ghost_set =np.zeros(visibility_map.shape)
        
        for ghost in ghosts:
            ghost_set[ghost[0]][ghost[1]] = 1
        
        ghost_maps = []
        ghost_maps.append(ghost_set)
        for i in range(look_ahead+1):
            prev_ghost_set = ghost_set
            ghost_set = np.zeros(visibility_map.shape)
            prev_ghosts = list(set(ghosts))
            ghosts=[]
            for ghost in prev_ghosts:
                ghosts.append(ghost)
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
            ghost_maps.append(ghost_set)

        pacman_maps = np.zeros((look_ahead+1, visibility_map.shape[0], visibility_map.shape[1])      )  
        # action_prob_map = []
        # final_action_map = []
        pacman_maps[look_ahead] = ghost_maps[look_ahead]*look_ahead
        pacman_maps[look_ahead][pacman_maps[look_ahead] == 0] = look_ahead+1
        level = look_ahead-1
        
        final_actions = []
        while level >=0:
            # cells = np.array(np.where(visibility_map!='?')).T.tolist()
            pacman_safety_map = np.ones(visibility_map.shape)*level
            # pacman_safety_map = look_ahead+1
            # action_prob = {}
            # final_action = np.copy(visibility_map)
            for action in ACTIONS:
                # action_safety_map = np.zeros(visibility_map.shape)
                # for i in range(len(transition_prob[action])):

                temp = np.zeros(visibility_map.shape)
                b_check = np.ones(visibility_map.shape)
                if action=="North":
                    dist = 1
                    axis = 0
                    b_check[0][:] = 0
                elif action=="West":
                    dist = 1
                    axis = 1
                    b_check[:][0] = 0
                elif action=="East":
                    dist = -1
                    axis = 1
                    b_check[:][-1] = 0
                elif action=="South":
                    dist = -1
                    axis = 0
                    b_check[-1][:] = 0
                elif action=="Stop":
                    dist=0
                    axis=0
                else:
                    print("INVALID ACTION")
                vis_shift = np.roll(visibility_map, dist, axis=axis)
                pacman_shift = np.roll(pacman_maps[level+1], dist,axis=axis)
                # b_check[0][:] = 0
                # print(b_check.shape)
                # print(vis_shift.shape)
                # print(visibility_map.shape)
                
                # mask = np.array(vis_shift != '?')
                mask = np.logical_and(np.array(visibility_map!='?'), np.array(vis_shift != '?'))
                mask = np.logical_and(mask, b_check)
                print("Action Safety", level, action)
                # for line in mask:
                #     l = [str(int(i)) for i in line]
                #     print(''.join(l))
                # print()
                # for line in mask:
                #     l = [str(int(i==True)) for i in line]
                #     print(''.join(l))
                # print()
                # for line in mask:
                #     l = [str(int(i==False)) for i in line]
                #     print(''.join(l))
                # print()
                # print(transition_prob[action][i])
                # print(pacman_shift.shape)
                # temp = (pacman_shift*(mask == True) + pacman_maps[level+1]*(mask==False))
                temp = (pacman_shift*(mask == True) + np.ones(visibility_map.shape)*(mask==False)*level)
                temp[visibility_map == '?'] = level
                temp[ghost_maps[level] == 1] = level
                # action_safety_map = np.maximum(action_safety_map, temp)
                # action_safety_map += temp
                # action_safety_map[visibility_map == '?'] = 1
                # action_safety_map[ghost_maps[level] == 1] = 1
                
                # for line in action_safety_map:
                #     l = [str(int(i)) for i in line]
                #     print(''.join(l))
                # print()
                # for i in range(LOOK_AHEAD+1):
                # plt.imshow(action_safety_map)
                # plt.colorbar()
                # plt.show()
                # action_safety_map[visibility_map=='?'] = 1
                    
                # pacman_safety_map = np.minimum(action_safety_map, pacman_safety_map)
                pacman_safety_map = np.maximum(temp, pacman_safety_map)
                # final_action[pacman_safety_map==action_safety_map] = action[0]
                # action_prob[action] = action_safety_map
            # final_action[visibility_map == '?'] = '?'
            # print("Final Action: ")
            # print(final_action)
            # action_prob_map.insert(0, action_prob)     
            # final_action_map.insert(0, final_action)
            # pacman_safety_map[ghost_maps[level] == 1] = 1
            # pacman_safety_map[visibility_map == '%'] = 4
            # pacman_safety_map[visibility_map == '?'] = 1
            pacman_maps[level] = pacman_safety_map                       
            level -= 1
        safety_map = pacman_maps[0]
        # action_map = action_prob_map[0]  
        pacmans = getPacman(visibility_map)
        print(pacmans)
        if look_ahead > 0:
            for pacman in pacmans:
                if pacman_maps[1][pacman[0]-1][pacman[1]] > look_ahead:
                    final_actions.append("North")
                if pacman_maps[1][pacman[0]][pacman[1]-1] > look_ahead:
                    final_actions.append("West")
                if pacman_maps[1][pacman[0]][pacman[1]+1] > look_ahead:
                    final_actions.append("East")
                if pacman_maps[1][pacman[0]+1][pacman[1]] > look_ahead:
                    final_actions.append("South")
                if pacman_maps[1][pacman[0]][pacman[1]] > look_ahead:
                    final_actions.append("Stop")
                print("North :", pacman_maps[1][pacman[0]-1][pacman[1]])
                print("West :", pacman_maps[1][pacman[0]][pacman[1]-1])
                print("East :", pacman_maps[1][pacman[0]][pacman[1]+1])
                print("South :", pacman_maps[1][pacman[0]+1][pacman[1]])
                print("Stop :", pacman_maps[1][pacman[0]][pacman[1]])
        print(final_actions)
        return final_actions

        
def render(safety_map):
    plt.imshow(safety_map)
    plt.colorbar()
    plt.show()

def main():
    layout = getLayout(layout_path=layout_path)
    print(getLayout(layout_path=layout_path))
    print()
    pacmans = getPacman(layout=layout)
    print(pacmans)
    print()
    ghosts = getGhost(layout=layout)
    print(ghosts)
    print()
    # prob_map = initMap(layout=layout)
    # print(prob_map)
    visibility_map = getVisibilityMap(layout=layout, pacmans=pacmans)
    print("Vismap")
    for line in visibility_map:
        print(''.join(line))
    safety_map, action_map = getSafetyMap(
        visibility_map=visibility_map
    )
    final_actions = getSafeActions(visibility_map=visibility_map, legalActions=ACTIONS, look_ahead=LOOK_AHEAD)
    # print("Safety map")
    # for line in safety_map:
    #     cseq = [str(int(i)) for i in line]
    #     print(''.join(cseq))
        
    # print("Action map")
    # for action in action_map.keys():
    #     print(action)
    #     for line in action_map[action]:
    #         cseq = [str(int(i)) for i in line]
    #         print(''.join(cseq))
    # for pacman in pacmans:
    #     print("Pacman: ", pacman)
    #     print("North :", action_map["North"][pacman[0]-1][pacman[1]])
    #     print("West :", action_map["West"][pacman[0]][pacman[1]-1])
    #     print("East :", action_map["East"][pacman[0]][pacman[1]+1])
    #     print("South :", action_map["South"][pacman[0]+1][pacman[1]])
    #     print("Stop :", action_map["Stop"][pacman[0]][pacman[1]])
    render(safety_map=safety_map)

if __name__=="__main__":
    main()