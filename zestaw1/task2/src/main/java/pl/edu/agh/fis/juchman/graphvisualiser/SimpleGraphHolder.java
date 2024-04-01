package pl.edu.agh.fis.juchman.graphvisualiser;

import org.jgrapht.ListenableGraph;
import org.jgrapht.ext.JGraphXAdapter;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.DefaultListenableGraph;
import org.jgrapht.graph.SimpleDirectedGraph;

public class SimpleGraphHolder implements GraphHolder<String, DefaultEdge>{

    ListenableGraph<String, DefaultEdge> innerGraph = new DefaultListenableGraph<>(new SimpleDirectedGraph<>(DefaultEdge.class));

    @Override
    public ListenableGraph<String, DefaultEdge> exposeInnerGraph() {
        return innerGraph;
    }

    @Override
    public JGraphXAdapter<String, DefaultEdge> getJgraphxRepresentation() {
        return new JGraphXAdapter<>(innerGraph);
    }
}
