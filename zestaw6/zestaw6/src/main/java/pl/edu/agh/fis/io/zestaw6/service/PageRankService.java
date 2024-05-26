package pl.edu.agh.fis.io.zestaw6.service;

import org.jgrapht.Graph;
import org.jgrapht.Graphs;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;


import java.util.HashMap;
import java.util.Map;
import java.util.Random;

@Service
public class PageRankService {

    private static final Logger logger = LoggerFactory.getLogger(PageRankService.class);


    public Graph<String, DefaultEdge> createGraph(String graphData) {
        Graph<String, DefaultEdge> graph = new DefaultDirectedGraph<>(DefaultEdge.class);
        if (graphData != null && !graphData.isEmpty()) {
            String[] lines = graphData.split("\\r?\\n");
            for (String line : lines) {
                String[] parts = line.split(":");
                try {
                    String source = parts[0].trim();
                    graph.addVertex(source);
                    if (parts.length > 1) {
                        String[] targets = parts[1].split(",");
                        for (String target : targets) {
                            target = target.trim();
                            graph.addVertex(target);
                            graph.addEdge(source, target);
                        }
                    }
                } catch (Exception e) {
                    logger.error("Skipping malformed line: {}", line, e);
                }
            }
        }
        return graph;
    }

    public Graph<String, DefaultEdge> createRandomGraph(int vertices, int edges) { /// TODO: TO TYLKO KOD POMOCNICZY, NIE MA GWARANCJI ŻE ZAPEWNIA GRAF O WŁAŚCIWOŚCIACH WYMAGANYCH PRZEZ ALGORYTM, NALEŻY KORZYSTAC Z `createGraph` I RĘCZNIE PODAC LISTE SĄSIEDZTWA
        Graph<String, DefaultEdge> graph = new DefaultDirectedGraph<>(DefaultEdge.class);
        Random random = new Random();
        for (int i = 0; i < vertices; i++) {
            graph.addVertex("" + i);
        }
        int edgeCount = 0;
        while (edgeCount < edges) {
            String source = "" + random.nextInt(vertices);
            String target = "" + random.nextInt(vertices);
            if (!source.equals(target) && !graph.containsEdge(source, target)) {
                graph.addEdge(source, target);
                edgeCount++;
            }
        }
        return graph;
    }

    public Map<String, Double> calculatePageRankRandomWalk(Graph<String, DefaultEdge> graph, int steps) {
        final double teleportProbability = 0.15;
        Map<String, Double> pageRank = new HashMap<>();
        int verticesCount = graph.vertexSet().size();
        if (verticesCount == 0) return pageRank;

        Random random = new Random();
        String[] vertices = graph.vertexSet().toArray(new String[0]);
        String currentVertex = vertices[random.nextInt(verticesCount)];

        for (int i = 0; i < steps; i++) {
            if (random.nextDouble() < teleportProbability) {
                currentVertex = vertices[random.nextInt(verticesCount)];
            } else {
                var edges = graph.outgoingEdgesOf(currentVertex);
                if (edges.isEmpty()) {
                    currentVertex = vertices[random.nextInt(verticesCount)];
                } else {
                    String finalCurrentVertex = currentVertex;
                    List<String> targets = edges.stream()
                            .map(edge -> Graphs.getOppositeVertex(graph, edge, finalCurrentVertex))
                            .toList();
                    currentVertex = targets.get(random.nextInt(targets.size()));
                }
            }
            pageRank.put(currentVertex, pageRank.getOrDefault(currentVertex, 0.0) + 1.0 / steps);
        }

        return pageRank;
    }

    public Map<String, Double> calculatePageRankIterative(Graph<String, DefaultEdge> graph, int iterations) {
        final double dampingFactor = 0.15;
        int verticesCount = graph.vertexSet().size();
        if (verticesCount == 0) return new HashMap<>();

        String[] vertices = graph.vertexSet().toArray(new String[0]);
        Map<String, Integer> vertexIndexMap = new HashMap<>();
        for (int i = 0; i < verticesCount; i++) {
            vertexIndexMap.put(vertices[i], i);
        }

        double[] rank = new double[verticesCount];
        double[] newRank = new double[verticesCount];
        double initialRank = 1.0 / verticesCount;
        double convergenceThreshold = 1e-6;

        Arrays.fill(rank, initialRank);
        double[][] P = new double[verticesCount][verticesCount];
        for (String source : vertices) {
            final int i = vertexIndexMap.get(source);
            var outgoingEdges = graph.outgoingEdgesOf(source);
            int outDegree = outgoingEdges.size();
            for (int j = 0; j < verticesCount; j++) {
                P[j][i] = dampingFactor / verticesCount;
            }
            if (outDegree > 0) {
                double linkProbability = (1 - dampingFactor) / outDegree;
                for (DefaultEdge edge : outgoingEdges) {
                    String target = Graphs.getOppositeVertex(graph, edge, source);
                    final int j = vertexIndexMap.get(target);
                    P[j][i] += linkProbability;
                }
            }
        }

        for (int iteration = 0; iteration < iterations; iteration++) {
            for (int j = 0; j < verticesCount; j++) {
                newRank[j] = 0.0;
                for (int i = 0; i < verticesCount; i++) {
                    newRank[j] += rank[i] * P[j][i];
                }
            }

            double maxChange = 0.0;
            for (int j = 0; j < verticesCount; j++) {
                maxChange = Math.max(maxChange, Math.abs(newRank[j] - rank[j]));
            }
            System.arraycopy(newRank, 0, rank, 0, verticesCount);
            if (maxChange < convergenceThreshold) {
                logger.info("Converged after {} iterations.", iteration + 1);
                break;
            }
        }

        return IntStream.range(0, verticesCount)
                .boxed()
                .collect(Collectors.toMap(i -> vertices[i], i -> rank[i]));
    }
}