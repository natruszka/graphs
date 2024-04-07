package pl.edu.agh.fis.juchman.graphvisualiser;

import org.jgrapht.graph.DefaultEdge;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.Config;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.ConfigFactory;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.GraphSourceType;
import pl.edu.agh.fis.juchman.graphvisualiser.display.GraphDisplay;
import pl.edu.agh.fis.juchman.graphvisualiser.graph.AttributedEdge;
import pl.edu.agh.fis.juchman.graphvisualiser.graph.GraphHolder;
import pl.edu.agh.fis.juchman.graphvisualiser.input.DotFileSource;
import pl.edu.agh.fis.juchman.graphvisualiser.input.GraphSource;
import pl.edu.agh.fis.juchman.graphvisualiser.input.SimpleGraphSourceFactory;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Objects;

public class GraphVisualiser {
    public static void main(String[] args){
        try
        {
            /// Config passed as an argument, makes this program entirely invokable by another separate program (eg. with dynamically created config)
            Config config = (args.length!=0)? ConfigFactory.createConfig(URI.create(args[0])) : ConfigFactory.createConfig(Objects.requireNonNull(GraphVisualiser.class.getResource("conf.toml")).toURI());

            if(config.graphSourceType() == GraphSourceType.DOT_FILE){
                DotFileSource dotFileSource = new DotFileSource(config);
                GraphHolder<String, AttributedEdge> graph = dotFileSource.getGraph();
                GraphDisplay.display(config.sceneSetup(),graph);
            }else{
                GraphSource<String,DefaultEdge> graphSource = SimpleGraphSourceFactory.createFromConfig(config);
                GraphHolder<String,DefaultEdge> graph = graphSource.getGraph();
                GraphDisplay.display(config.sceneSetup(),graph);
            }


        }catch (URISyntaxException uriSyntaxException){System.exit(0);}
    }
}
