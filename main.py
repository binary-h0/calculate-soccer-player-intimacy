# -*- coding: utf-8 -*-
from konlp.kma.klt2023 import klt2023
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(10**9)
# TODO 가중치 추가하기


class SPI():
    def __init__(self):
        self.soccer_player_url = 'soccer-player-intimacy/src/soccer_player.txt'
        self.soccer_player_lis = []
        self.soccer_player = self.getSoccerPlayer()
        self.n = len(self.soccer_player)
        self.graph = [[0 for _ in range(self.n)] for __ in range(self.n)]
        self.edges = set()
        self.visited = [False for _ in range(self.n)]
        self.parents = [i for i in range(self.n)]
        self.G = nx.Graph()

    def getSoccerPlayer(self):
        soccer_player = dict()
        with open(self.soccer_player_url, 'r', encoding='utf-8') as f:
            player = f.readline().rstrip()
            while player:
                soccer_player[player] = len(soccer_player)
                self.soccer_player_lis.append(player)
                player = f.readline().rstrip()
            f.close()
        return soccer_player

    def getMorphsResult(self, src):
        klt = klt2023()
        result = []
        with open(src, 'r', encoding='utf-8') as f:
            text = f.read()
            result = klt.morphs(text)
        return result

    def updateGraph(self, morphs):
        tmp_player_lis = set()
        for word in morphs:
            if word in self.soccer_player:
                tmp_player_lis.add(word)
            else:
                # if word == "연습":
                #     print("HIT")
                pass
        for comb in combinations(tmp_player_lis, 2):
            p1, p2 = comb
            pn1, pn2 = self.soccer_player[p1], self.soccer_player[p2]
            self.graph[pn1][pn2] += 1
            self.graph[pn2][pn1] += 1
            self.edges.add((p1, p2, 1))

    def find(self, x):
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x < y:
            self.parents[y] = x
        else:
            self.parents[x] = y

    def union_find(self):
        for edge in self.edges:
            p1, p2, w = edge
            p1, p2 = self.soccer_player[p1], self.soccer_player[p2]
            if self.find(p1) != self.find(p2):
                self.union(p1, p2)

    def dfs(self, player_i):
        self.visited[player_i] = True
        self.G.add_node(self.soccer_player_lis[player_i])
        num = 1
        for next_player_i in range(self.n):
            if self.graph[player_i][next_player_i] == 0:
                continue
            if not self.visited[next_player_i]:
                num += self.dfs(next_player_i)
                self.G.add_edge(self.soccer_player_lis[player_i], self.soccer_player_lis[next_player_i],
                                weight=self.graph[player_i][next_player_i])
        return num

    def dfs_search(self):
        for player_i in range(self.n):
            if self.parents[player_i] != player_i:
                if not self.visited[player_i]:
                    self.dfs(player_i)


if __name__ == '__main__':
    spi = SPI()
    for i in range(0, 50):
        url = "soccer-player-intimacy/src/page%d_data.txt" % i
        morphs = spi.getMorphsResult(url)
        print(i)
        spi.updateGraph(morphs)
    spi.union_find()
    print(spi.parents)
    spi.dfs_search()

    pos = nx.kamada_kawai_layout(spi.G)
    nx.draw_kamada_kawai(spi.G)
    nx.draw_networkx_labels(
        spi.G, pos, font_family='NanumGothic', font_size=10)
    labels = nx.get_edge_attributes(spi.G, 'weight')
    nx.draw_networkx_edge_labels(spi.G, pos, edge_labels=labels)
    plt.show()
    for i in range(spi.n):
        print(spi.graph[i])
