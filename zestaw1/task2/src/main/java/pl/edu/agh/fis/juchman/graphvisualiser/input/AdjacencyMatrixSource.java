package pl.edu.agh.fis.juchman.graphvisualiser.input;

import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.util.SupplierUtil;
import pl.edu.agh.fis.juchman.graphvisualiser.graph.GraphHolder;
import pl.edu.agh.fis.juchman.graphvisualiser.graph.SimpleGraphHolder;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.Config;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Scanner;

class AdjacencyMatrixSource implements GraphSource<String, DefaultEdge>{
    private final Config config;
    private final SimpleGraphHolder<String,DefaultEdge> graphHolder;
    private int vertexCount;
    private int edgeCount;

    public AdjacencyMatrixSource(Config config) {
        this.config = config;
        this.graphHolder = new SimpleGraphHolder<>(SupplierUtil.createStringSupplier(),SupplierUtil.createDefaultEdgeSupplier());
    }

    @Override
    public GraphHolder<String, DefaultEdge> getGraph() { 
        boolean isGraphEmpty = graphHolder.exposeInnerGraph().vertexSet().isEmpty();
        boolean wasGraphUpdated = vertexCount != graphHolder.exposeInnerGraph().vertexSet().size() || edgeCount != graphHolder.exposeInnerGraph().edgeSet().size();
        if( isGraphEmpty || wasGraphUpdated){
            try {
                Scanner scanner = new Scanner(Path.of(config.graphSourceUri()));
                String[] vertices = scanner.next().split(config.lineElementSeparator()); 
                int verticesCount = vertices.length;
                for (int i = 0; i < verticesCount; ++i) {
                    graphHolder.exposeInnerGraph().addVertex(String.valueOf(i));
                }
                for (int i = 0; scanner.hasNext(); ++i) { 
                    for (int j = 0; j < verticesCount; ++j) {
                        if (vertices[j].equals("1")){
                            graphHolder.exposeInnerGraph().addEdge(String.valueOf(i), String.valueOf(j));
                        }
                    }
                    vertices = scanner.next().split(config.lineElementSeparator());
                }
                vertexCount = graphHolder.exposeInnerGraph().vertexSet().size();
                edgeCount = graphHolder.exposeInnerGraph().edgeSet().size();
            }catch(IOException ioException){throw new RuntimeException(ioException);}
        }
        return graphHolder;

    }
}
