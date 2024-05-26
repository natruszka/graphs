package pl.edu.agh.fis.io.zestaw6.controller;

import org.jgrapht.Graph;
import org.jgrapht.graph.DefaultEdge;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import pl.edu.agh.fis.io.zestaw6.model.GraphForm;
import pl.edu.agh.fis.io.zestaw6.service.PageRankService;
import pl.edu.agh.fis.io.zestaw6.service.TspService;

import java.io.IOException;
import java.util.Map;
import java.util.stream.Collectors;

@Controller
public class ZestawController {

    PageRankService pageRankService;
    private TspService tspService;
    private Graph<String,DefaultEdge> graph;

    @Autowired
    public ZestawController(PageRankService pageRankService, TspService tspService) {
        this.pageRankService = pageRankService;
        this.tspService = tspService;
    }

    @GetMapping("/")
    public String landingPage(Model model){
        return "index";
    }
    @GetMapping("/pagerank")
    public String getPageRankForm(Model model) {
        model.addAttribute("graphForm", new GraphForm());
        return "pagerank";
    }

    @PostMapping("/pagerank")
    public String calculatePageRank(@ModelAttribute GraphForm graphForm, Model model) {
        graph = pageRankService.createGraph(graphForm.getGraphData());
        prepareModelForVisualization(graph, model);
        model.addAttribute("graphForm", new GraphForm());

        return "pagerank";
    }

    @PostMapping("/pagerank/random")
    public String generateRandomGraph(@RequestParam int vertices, @RequestParam int edges, Model model) {
        graph = pageRankService.createRandomGraph(vertices, edges);
        prepareModelForVisualization(graph, model);
        model.addAttribute("graphForm", new GraphForm());

        return "pagerank";
    }

    @PostMapping("/pagerank/calculate")
    public String calculatePageRank(@RequestParam int steps, @RequestParam int iterations,@RequestParam double tel_prob, Model model) {
        if(graph == null){
            return "pagerank";
        }
        model.addAttribute("pagerankIterative",pageRankService.calculatePageRankIterative(graph,iterations));
        model.addAttribute("pagerankRandomWalk",pageRankService.calculatePageRankRandomWalk(graph,steps));
        prepareModelForVisualization(graph, model);
        model.addAttribute("graphForm", new GraphForm());

        return "pagerank";
    }

    @GetMapping("/tsp")
    public String index() {
        return "tsp";
    }

    @PostMapping("/tsp/upload")
    public String uploadFile(@RequestParam("file") MultipartFile file, Model model) throws IOException {
        tspService.loadCoordinatesFromFile(file);
        tspService.calculateShortestPath();

        model.addAttribute("coordinates", tspService.getCoordinates());
        model.addAttribute("initialPath", tspService.getInitialPath());
        model.addAttribute("finalPath", tspService.getFinalPath());
        model.addAttribute("initialLength", tspService.calculateTotalDistance(tspService.getInitialPath()));
        model.addAttribute("finalLength", tspService.calculateTotalDistance(tspService.getFinalPath()));
        return "tspresult";
    }

        private void prepareModelForVisualization(Graph<String, DefaultEdge> graph, Model model) {
        var nodes = graph.vertexSet().stream()
                .map(v -> Map.of("id", v, "group", 1))
                .collect(Collectors.toList());

        var links = graph.edgeSet().stream()
                .map(e -> Map.of("source", graph.getEdgeSource(e), "target", graph.getEdgeTarget(e)))
                .collect(Collectors.toList());

        model.addAttribute("nodes", nodes);
        model.addAttribute("links", links);
    }
}