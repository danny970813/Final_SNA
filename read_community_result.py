from igraph import *
import csv

path = './data/hero-network.csv'
Louvain_community_path = './result/Louvain_community_result.csv'
GEMSEC_community_path = './result/GEMSEC_community_result.csv'
RGB_path = './data/RGB.txt'

def get_community(community_path):

    community_list, name_list, num_hero_list, pr_list, center_list = [], [], [], [], []
    # 開啟 CSV 檔案
    with open(community_path, "r",newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        rows = list(rows)
        """
        ['hero', 'num_hero', 'community', 'pr', 'center','modularit:' + str(g.modularity(result))]
        """
        if len(rows[0])==6:
            modularity = rows[0][5]
        else:
            modularity = None
        for row in rows[1:]:
            # name = row[0]
            # num_hero = row[1]
            # print('row[2]', row[2], type(row[2]))
            community = int(row[2])
            pr = float(row[3])
            center = row[4]
            # name_list.append(name)
            # num_hero_list.append(num_hero)
            community_list.append(community)
            pr_list.append(pr)
            center_list.append(center)
        element =[]
        # element.append(name_list[1:])
        # element.append(num_hero_list[1:])
        element.append(community_list)
        element.append(pr_list)
        element.append(center_list)
        element.append(modularity)
    
    return element

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

def get_RGB_list(list):
    color = []
    for content in list:
        data = content.replace('\t', ' ').split(' ')
        temp = []
        string = []
        for count, i in enumerate(data):
            if not i == '' :
                if len(temp)<3:
                    temp.append(i)
                else:
                    string.append(i)
        name = ''
        for i in string:
            name = name + i + ' '
        temp.append(name[:-1])
        color.append(temp[3])
        # print('RGB', temp)

    return color

def main():
    
    data = input(path)
    edges, vertic = create_relate(data)
    # print('')
    # edges = delete_repeat(edges)
    n_nodes = len(vertic)

    #---------------------create graph---------------------
    g = Graph()
    g.add_vertices(n_nodes)
    g.add_edges(edges)
    summary(g)
    g = g.simplify()
    summary(g)

    #---------------------graph information---------------------
    element = get_community(GEMSEC_community_path) #choices Louvain_community_path or GEMSEC_community_path
    degree = g.degree()
    g.vs['degree'] = degree
    g.vs["name"] = list(vertic.keys())
    g.vs["community"] = element[0]
    g.vs["pr"] = element[1]
    g.vs["center"] = element[2]

    modularity = element[3]
    n_community = max(g.vs['community']) + 1
    

    print(g.vs[0].attributes())
    print(g.vs[1].attributes())
    print(g.vs[2].attributes())

    # pal = drawing.colors.ClusterColoringPalette(max(g.vs['community'])+1)
    # g.vs['color'] = pal.get_many(i.membership)
    # plot(g)

    #---------------------visual information---------------------
    
    RGB = input(RGB_path)
    color_list = get_RGB_list(RGB)
    color_dict = {}
    size = []
    for i in range(n_community):
        color_dict[i] = color_list[i*3]

    for v in g.vs['degree']:
        if v >= 200:
            size.append(30)
        elif v >= 100:
            size.append(10)
        else:
            size.append(1)
    

    layout = g.layout("kk")

    visual_style = {}
    g.vs["color"] = [color_dict[C] for C in g.vs["community"]]
    visual_style["edge_width"] = 0.1
    visual_style["vertex_size"] = size
    # visual_style["vertex_size"] = [(D**0.5)*P for D, P in zip(g.vs["degree"], g.vs["pr"])]
    visual_style["layout"] = layout
    #---------------------------plot--------------------------
    
    # g.vs["label"] = g.vs["name"]
    plot(g, "./result/kk_D200_E0.1_graph01.png", mark_groups = True, **visual_style)
        

    
if __name__ == '__main__':
    main()