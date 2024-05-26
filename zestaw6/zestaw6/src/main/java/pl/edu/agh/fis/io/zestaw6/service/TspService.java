package pl.edu.agh.fis.io.zestaw6.service;

import org.jgrapht.Graph;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.SimpleWeightedGraph;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

@Service
public class TspService {

    private final int MAX_ITER = 5000;
    private List<double[]> coordinates = new ArrayList<>();
    private List<Integer> initialPath;
    private List<Integer> finalPath;

    public void loadCoordinatesFromFile(MultipartFile file) throws IOException {
        coordinates.clear();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(file.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(" ");
                double x = Double.parseDouble(parts[0]);
                double y = Double.parseDouble(parts[1]);
                coordinates.add(new double[]{x, y});
            }
        }
    }

    public List<double[]> getCoordinates() {
        return coordinates;
    }

    public List<Integer> getInitialPath() {
        return initialPath;
    }

    public List<Integer> getFinalPath() {
        return finalPath;
    }

    public void calculateShortestPath() {
        Graph<Integer, DefaultEdge> graph = createGraph();
        List<Integer> vertices = new ArrayList<>(graph.vertexSet());

        initialPath = generateInitialPath(vertices);
        List<Integer> currentPath = new ArrayList<>(initialPath);
        double currentDistance = calculateTotalDistance(graph, currentPath);
        double temperature;

        Random random = new Random();

        for (int i = 100; i > 1; i--) {
            temperature = 0.001 * i * i;
            for (int it = 0; it < MAX_ITER; it++) {
                List<Integer> newPath = new ArrayList<>(currentPath);
                perform2OptSwap(newPath);

                double newDistance = calculateTotalDistance(graph, newPath);

                if (acceptanceProbability(currentDistance, newDistance, temperature) > random.nextDouble()) {
                    currentPath = new ArrayList<>(newPath);
                    currentDistance = newDistance;
                }
            }
        }

        finalPath = new ArrayList<>(currentPath);
    }

    public double calculateTotalDistance(List<Integer> path) {
        Graph<Integer, DefaultEdge> graph = createGraph();
        double totalDistance = 0;
        for (int i = 0; i < path.size() - 1; i++) {
            totalDistance += graph.getEdgeWeight(graph.getEdge(path.get(i), path.get(i + 1)));
        }
        totalDistance += graph.getEdgeWeight(graph.getEdge(path.get(path.size() - 1), path.get(0)));
        return totalDistance;
    }

    private Graph<Integer, DefaultEdge> createGraph() {
        Graph<Integer, DefaultEdge> graph = new SimpleWeightedGraph<>(DefaultEdge.class);
        for (int i = 0; i < coordinates.size(); i++) {
            graph.addVertex(i);
        }
        for (int i = 0; i < coordinates.size(); i++) {
            for (int j = i + 1; j < coordinates.size(); j++) {
                graph.setEdgeWeight(graph.addEdge(i, j), distanceBetween(coordinates.get(i), coordinates.get(j)));
            }
        }
        return graph;
    }

    private double distanceBetween(double[] point1, double[] point2) {
        return Math.sqrt(Math.pow(point1[0] - point2[0], 2) + Math.pow(point1[1] - point2[1], 2));
    }

    private List<Integer> generateInitialPath(List<Integer> vertices) {
        List<Integer> initialPath = new ArrayList<>(vertices);
        Collections.shuffle(initialPath);
        return initialPath;
    }

    private double calculateTotalDistance(Graph<Integer, DefaultEdge> graph, List<Integer> path) {
        double totalDistance = 0;
        for (int i = 0; i < path.size() - 1; i++) {
            totalDistance += graph.getEdgeWeight(graph.getEdge(path.get(i), path.get(i + 1)));
        }
        totalDistance += graph.getEdgeWeight(graph.getEdge(path.get(path.size() - 1), path.get(0)));
        return totalDistance;
    }

    private void perform2OptSwap(List<Integer> path) {
        Random random = new Random();
        int i = random.nextInt(path.size());
        int j = random.nextInt(path.size());

        while (i == j) {
            j = random.nextInt(path.size());
        }

        if (i > j) {
            int temp = i;
            i = j;
            j = temp;
        }

        while (i < j) {
            Collections.swap(path, i, j);
            i++;
            j--;
        }
    }

    private double acceptanceProbability(double currentDistance, double newDistance, double temperature) {
        if (newDistance < currentDistance) {
            return 1.0;
        }
        return Math.exp((currentDistance - newDistance) / temperature);
    }
}
