package pl.edu.agh.fis.juchman.graphvisualiser.input;
import org.jgrapht.graph.DefaultEdge;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.Config;

public final class GraphSourceFactory { // takeses in config, and returns the right source.
    public static GraphSource<String, DefaultEdge> createFromConfig(Config config){
        return switch(config.graphSourceType()){
            case ADJACENCY_LIST -> new AdjacencyListSource(config) ;
            case ADJACENCY_MATRIX -> new AdjacencyMatrixSource(config);
            case INCIDENCE_MATRIX -> new IncidenceMatrixSource(config);
        };
    }
}