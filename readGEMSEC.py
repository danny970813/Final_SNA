"""
this program can read GEMSEC community result json file
and ouput ['hero', 'num_hero', 'community', 'pr', 'center'] csv file

"""
from igraph import *
import json
import csv
import os

path = './data/hero-network.csv'
num_path = './data/num_hero.csv'
result_path = './result/GEMSEC_community_result.csv'
json_path = './data/hero_10epoch.json'

def input(path):
    f = open(path, 'r')
    str = f.read()
    if str != '':
        dst_list = str.replace(', ', ' ').split('\n')
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

def check(edges, vertic):
    for e in edges:
        for v in e:
            if not v in vertic:
                print('loss:', v)
    print('check pass')

def remove_noise(edges):
    return 0

def main():

    folder = os.path.exists('./result')
    if not folder:
        #如果不存在，則建立新目錄
        os.makedirs('./result')
    
    data = input(path)
    edges, vertic = create_relate(data)
    num_vertic = len(vertic)

    g = Graph()
    g.add_vertices(num_vertic)
    g.add_edges(edges)
    summary(g)

    g.vs["name"] = list(vertic.keys())
        
    with open(json_path , 'r') as reader:
        jf = json.loads(reader.read())

    community = []

    for i in range(num_vertic):
        community.append(jf[str(i)])

    g.vs["community"] = community

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

    result_str = []
    title = ['hero', 'num_hero', 'community', 'pr', 'center']
    result_str.append(title)

    for i in range(num_vertic):
        content = [g.vs[i]['name'], str(i), str(g.vs[i]['community']), g.vs[i]['pr'], g.vs[i]['center']]
        result_str.append(content)

    with open(result_path, "w", newline="") as csvfile:
        wr = csv.writer(csvfile)
        wr.writerows(result_str)

    
if __name__ == '__main__':
    main()