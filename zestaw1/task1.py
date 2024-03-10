#!/usr/bin/python

# ZADANIE 1
# Napisać program kodujący grafy proste za pomocą macierzy sąsiedztwa, 
# macierzy incydencji i list sąsiędztwa. Stworzyć moduł do zmiany
# danego kodowania na pozostałe.
# Autor: Glib Bers

import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class RGraph():
    def __init__(self):
        self.data = []
        self.representation = "Adjacency matrix"
        self.length = 0

    def to_adjacency_matrix(self):

        if (self.representation == "Adjacency matrix"):
            print("This graph is already represented by an adjacency matrix")

        elif(self.representation == "Adjacency list"):
            newdata = [[0 for _ in range(self.length)] for i in range(self.length)]
            for node, neighbour in self.data.items:
                newdata[node][neighbour] = 1
                newdata[neighbour][node] = 1
            self.data = newdata
            self.representation = "Adjacency matrix"

        elif(self.representation == "Incident matrix"):
            newdata = [[0 for j in range(self.length)] for i in range(self.length)]
            for i in range(self.length):
                for j in range(i, self.length):
                    n_sum = 0
                    for col in range(len(self.data[0])):
                        n_sum += self.data[i][col]*self.data[j][col]
                    newdata[i][j] = 0 if i == j else n_sum
                    newdata[j][i] = 0 if i == j else n_sum
            self.data = newdata
            self.representation = "Adjacency matrix"



    def to_adjacency_list(self):

        if (self.representation == "Adjacency matrix"):
            newdata = {}
            for i in range(self.length):
                newdata[i] = [j for j in range(self.length) if self.data[i][j] == 1]
            self.data = newdata
            self.representation = "Adjacency list"

        elif(self.representation == "Adjacency list"):
            print("This graph is already represented by an adjacency list")

        elif(self.representation == "Incident matrix"):
            self.to_adjacency_matrix()
            self.to_adjacency_list()
            self.representation = "Adjacency list"



    def to_incident_matrix(self):

        if (self.representation == "Adjacency matrix"):
            newdata = []
            for i in range(self.length):
                for j in range(i, self.length):
                    if (self.data[i][j] == 1):
                        newdata.append([1 if (k==i or k==j) else 0 for k in range(self.length)])

            newdata = np.transpose(newdata)
            self.data = newdata
            self.representation = "Incident matrix"

        elif(self.representation == "Adjacency list"):
            self.to_adjacency_matrix()
            self.to_incident_matrix()
            self.representation = "Incident matrix"

        elif(self.representation == "Incident matrix"):
            print("This graph is already represented by an incident matrix")



    def graph_from_file(self, filename, representation):
        self.data = []
        self.representation = representation

        if (representation == "Adjacency matrix"):
            with open(filename, "r") as input_file:
                lines = input_file.readlines()

                for line in lines:
                    self.data.append(list(map(int, line.split())))

            self.length = len(self.data)

        elif (representation == "Adjacency list"):
            data = {}
            with open(filename, "r") as input_file:
                lines = input_file.readlines()

                for line in lines:
                    data[line.split('.')[0]] = list(map(int, line.split('.')[1]))
                    
            self.length = len(self.data)
                    
        elif (representation == "Incident matrix"):
            with open(filename, "r") as input_file:
                lines = input_file.readlines()

                for line in lines:
                    self.data.append(list(map(int, line.split())))
                    
            self.length = len(self.data[0])

    def print(self):
        print(self.data)


RG = RGraph()
RG.graph_from_file("input.txt", "Adjacency matrix")
RG.print()

RG.to_adjacency_matrix()
RG.print()

RG.to_incident_matrix()
RG.print()

RG.to_adjacency_list()
RG.print()