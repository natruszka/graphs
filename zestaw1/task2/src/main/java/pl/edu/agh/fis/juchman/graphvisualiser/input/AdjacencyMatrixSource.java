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

    @Override ///TODO !!!this is an old and dumb approach, I was too lazy to rewrite it, in other inputs I use a nicer approach.
    public GraphHolder<String, DefaultEdge> getGraph() { ///Please do have mercy on this poor naive function and ensure a nice and correct input :((
        boolean isGraphEmpty = graphHolder.exposeInnerGraph().vertexSet().isEmpty();
        boolean wasGraphUpdated = vertexCount != graphHolder.exposeInnerGraph().vertexSet().size() || edgeCount != graphHolder.exposeInnerGraph().edgeSet().size();
        if( isGraphEmpty || wasGraphUpdated){/// Hey, look! a wild optimization has appeared... and considering that we run the code only once its... hmm... useless?
            try {// Stupid checked exception!!! you only clutter this code :< (well... not as much as these comments)
                Scanner scanner = new Scanner(Path.of(config.graphSourceUri()));
                String[] vertices = scanner.next().split(config.lineElementSeparator()); /// God forbid you from running this on file with some stupid junk :< ... please
                int verticesCount = vertices.length; /// I sure hope so that is the case!
                for (int i = 0; i < verticesCount; ++i) {
                    graphHolder.exposeInnerGraph().addVertex(String.valueOf(i));
                }
                for (int i = 0; scanner.hasNext(); ++i) { //I could optimize it, but I will not exert myself ;>
                    for (int j = 0; j < verticesCount; ++j) {
                        if (vertices[j].equals("1")){
                            graphHolder.exposeInnerGraph().addEdge(String.valueOf(i), String.valueOf(j)); /// I really do not like this indentation, it is basically an arrow anti-patter :((( but I can't do anything about it >:[
                        }
                    }
                    vertices = scanner.next().split(config.lineElementSeparator());
                }
                vertexCount = graphHolder.exposeInnerGraph().vertexSet().size();
                edgeCount = graphHolder.exposeInnerGraph().edgeSet().size();
            }catch(IOException ioException){throw new RuntimeException(ioException); /* Sorry, too lazy to handle it any other way :> */}
        }
        return graphHolder;

    }
}
