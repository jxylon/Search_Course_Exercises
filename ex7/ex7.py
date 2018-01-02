# encoding='utf-8'
from pygraph.classes.digraph import digraph


class PRIterator:
    __doc__ = '计算一张图中的PR值'

    def __init__(self, dg):
        self.damping_factor = 0.85
        self.max_iterations = 100
        self.min_delta = 0.00001
        self.graph = dg

    def pagerank(self):
        # 生成闭环
        for node in self.graph.nodes():
            if (len(self.graph.neighbors(node)) == 0):
                for node2 in self.graph.nodes():
                    self.graph.add_edge(self.graph, (node, node2))
        nodes = self.graph.nodes()
        graph_size = len(nodes)
        # 如果图为空，直接退出
        if (graph_size == 0):
            return {}
        # page_rank 字典
        page_rank = dict.fromkeys(nodes, 1.0 / graph_size)
        # 阻尼系数(1-d)/N
        damping_value = (1.0 - self.damping_factor) / graph_size
        flag = False
        for i in range(self.max_iterations):
            change = 0
            for node in nodes:
                rank = 0
                for incident_page in self.graph.incidents(node):
                    rank += self.damping_factor * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                rank += damping_value
                change += abs(page_rank[node] - rank)
                page_rank[node] = rank
            print("%d iteration" % (i + 1))
            print(page_rank)
            if change < self.min_delta:
                flag = True
                break
        if (flag):
            print("finished in %d around" % (i+1))
        else:
            print("finished out of 100 iterations!")
        return page_rank


def read_graph(path):
    nodes, edges = [], []
    with open(path, 'r') as file:
        graph = file.readlines()
    for i in graph[1].split(' '):
        nodes.append(i)
    # 去掉最后一个元素
    nodes[-1] = nodes[-1].split('\n')[0]
    for i in graph[3:]:
        edge = i.split(' ')
        edge[1] = edge[1].split('\n')[0]
        edges.append(edge)
    return nodes, edges


if __name__ == '__main__':
    rootdir = 'D:/搜索引擎/exercise/ex7/'
    filename = 'pagerank_seven_nodes.txt'
    nodes, edges = read_graph(rootdir + filename)
    dg = digraph()
    dg.add_nodes(nodes)
    for edg in edges:
        dg.add_edge(edg)
    pri = PRIterator(dg)
    pagerank = pri.pagerank()
