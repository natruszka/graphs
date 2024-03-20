package pl.edu.agh.fis.juchman.graphvisualiser;

import org.jgrapht.graph.DefaultEdge;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.Config;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.ConfigFactory;
import pl.edu.agh.fis.juchman.graphvisualiser.display.GraphDisplay;
import pl.edu.agh.fis.juchman.graphvisualiser.input.GraphSource;
import pl.edu.agh.fis.juchman.graphvisualiser.input.GraphSourceFactory;

import java.io.FileNotFoundException;
import java.net.URISyntaxException;
import java.util.Objects;

public class GraphVisualiser {
    public static void main(String[] args){
        try{
            Config config = ConfigFactory.createConfig(Objects.requireNonNull(GraphVisualiser.class.getResource("conf.toml")).toURI()); //CreateConfig works with any valid URI pointing to the TOML config

            GraphSource<String,DefaultEdge> graphSource = GraphSourceFactory.createFromConfig(config);
            GraphHolder<String, DefaultEdge> graph = graphSource.getGraph();
            GraphDisplay.display(config.sceneSetup(),graph);

        }catch (URISyntaxException uriSyntaxException){System.exit(0);}
    }
}
