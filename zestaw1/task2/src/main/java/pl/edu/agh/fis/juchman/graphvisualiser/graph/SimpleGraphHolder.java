package pl.edu.agh.fis.juchman.graphvisualiser.graph;

import com.mxgraph.model.mxIGraphModel;
import com.mxgraph.util.mxConstants;
import org.jgrapht.Graph;
import org.jgrapht.ListenableGraph;
import org.jgrapht.ext.JGraphXAdapter;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultListenableGraph;

import java.util.function.Supplier;

public class SimpleGraphHolder<V,E> implements GraphHolder<V, E>{

    ListenableGraph<V, E> innerGraph;

    public SimpleGraphHolder(Supplier<V> vertexSupplier, Supplier<E> edgeSupplier) {
        Graph<V, E> baseGraph = new DefaultDirectedGraph<>(vertexSupplier, edgeSupplier, false);
        this.innerGraph = new DefaultListenableGraph<>(baseGraph);
    }

    @Override
    public ListenableGraph<V, E> exposeInnerGraph() {
        return innerGraph;
    }

    @Override
    public JGraphXAdapter<V, E> getJgraphxRepresentation() {
        JGraphXAdapter<V, E> adapter = new JGraphXAdapter<>(innerGraph);

        mxIGraphModel model = adapter.getModel();
        model.beginUpdate();
        try {
            Object[] edges = adapter.getChildEdges(adapter.getDefaultParent());
            for (Object edge : edges) {
                adapter.getModel().setStyle(edge, mxConstants.STYLE_NOLABEL + "=1");
            }
        } finally {
            model.endUpdate();
        }

        return adapter;
    }
}

