from igraph import *
import csv
import os

path = './data/hero-network.csv'
result_path = './result/Louvain_community_result.csv'

def input(path):
    f = open(path, 'r')
    str = f.read()
    if str != '':
        dst_list = str.split('\n')
        if dst_list[-1] == '':
            del dst_list[-1]
    else:
        dst_list = ['']
    f.close()
    
    return dst_list

def create_relate(list):
    vertic = {}
    edges = []
    count = 0
    for content in list[1:]:
        node = content.replace('"', '').split(',')

        if not node[0] in vertic.keys():
            vertic[node[0]] = count
            count = count + 1
        if not node[1] in vertic.keys():
            vertic[node[1]] = count
            count = count + 1

        node = [vertic[node[0]], vertic[node[1]]]
        edges.append(node)
        print( "edges: %d\r" % ( len(edges) ), end='' )

    return edges, vertic

def main():

    folder = os.path.exists('./result')
    if not folder:
        #如果不存在，則建立新目錄
        os.makedirs('./result')
    
    data = input(path)
    edges, vertic = create_relate(data)
    n_nodes = len(vertic)

    #---------------------create graph---------------------
    g = Graph()
    g.add_vertices(n_nodes)
    g.add_edges(edges)
    summary(g)

    #---------------------graph information---------------------

    g.vs["name"] = list(vertic.keys())
    degree = g.degree()
    g.vs['degree'] = degree
    print(g.vs[0].attributes())

    result=g.community_multilevel()

    print('modularity:', g.modularity(result))
    
    for count, community in enumerate(result):
        print( "community: %d\r" % ( count ), end='' )
        for node in community:
            g.vs[node]["community"] = count

    n_community = max( g.vs["community"]) + 1

    for i in range(n_community):
        C = g.vs.select(community_eq = i)
        sub_C = g.subgraph(C)
        sub_C.to_directed()
        pr_value = sub_C.pagerank()
        
        for count, v in enumerate(C):
            g.vs[v.index]['pr'] = pr_value[count]
        
        center_pr = max(pr_value)
    
        C_maxpr_index = pr_value.index(center_pr)
        g.vs[C[C_maxpr_index].index]['center'] = 1

    # M = g.vs.select(center_eq = 1)
    # for v in M:
    #     print(v.index)

    #========================================================

    result_str = []
    title = ['hero', 'num_hero', 'community', 'pr', 'center','modularit:' + str(g.modularity(result))]
    result_str.append(title)

    for i in range(n_nodes):
        content = [g.vs[i]['name'], str(i), str(g.vs[i]['community']), g.vs[i]['pr'], g.vs[i]['center']]
        result_str.append(content)

    with open(result_path, "w", newline="") as csvfile:
        wr = csv.writer(csvfile)
        wr.writerows(result_str)
        

    
if __name__ == '__main__':
    main()