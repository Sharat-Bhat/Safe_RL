from hashlib import new
from Environment import Environment
from SafetyRules import SafetyRules


def main():
    env = Environment(ndt_flag=True, ndt_prob=0.2)
    sp = SafetyRules()

    mdp_graph = env.MDPtoGraph()
    sp_graph = sp.SPtoGraph()

    sp.get_cross_graph(mdp_graph, sp_graph)


main()
