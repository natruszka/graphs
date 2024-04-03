package pl.edu.agh.fis.juchman.graphvisualiser.input;

import org.jgrapht.nio.dot.DOTImporter;
import java.io.FileReader;
import java.io.IOException;

import pl.edu.agh.fis.juchman.graphvisualiser.graph.AttributedEdge;
import pl.edu.agh.fis.juchman.graphvisualiser.graph.AttributedGraphHolder;
import pl.edu.agh.fis.juchman.graphvisualiser.graph.GraphHolder;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.Config;

public class DotFileSource implements GraphSource<String, AttributedEdge> {
    private final Config config;

    public DotFileSource(Config config) {
        this.config = config;
    }

    @Override
    public GraphHolder<String, AttributedEdge> getGraph() {
        AttributedGraphHolder graphHolder = new AttributedGraphHolder();

        DOTImporter<String, AttributedEdge> importer = new DOTImporter<>();
        importer.setVertexFactory(String::new);

        importer.setEdgeWithAttributesFactory(attrs -> {
            AttributedEdge edge = new AttributedEdge();
            if (attrs.containsKey("color")) {
                edge.setColor(attrs.get("color").getValue());
            }
            if (attrs.containsKey("penwidth")) {
                edge.setPenWidth(Float.parseFloat(attrs.get("penwidth").getValue()));
            }
            if (attrs.containsKey("weight")) {
                edge.setWeight(Double.parseDouble(attrs.get("weight").getValue()));
            }
            return edge;
        });

        try {
            importer.importGraph(graphHolder.exposeInnerGraph(), new FileReader(config.graphSourceUri().getPath()));
        } catch (IOException e) {
            throw new RuntimeException("There was an error while trying to import graph from DOT_FILE: " + config.graphSourceUri(), e);
        }

        return graphHolder;
    }
}
