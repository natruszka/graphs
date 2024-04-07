package pl.edu.agh.fis.juchman.graphvisualiser.graph;

import com.mxgraph.util.mxConstants;
import org.jgrapht.ListenableGraph;
import org.jgrapht.ext.JGraphXAdapter;
import org.jgrapht.graph.DefaultListenableGraph;
import org.jgrapht.graph.SimpleDirectedWeightedGraph;

public class AttributedGraphHolder implements GraphHolder<String, AttributedEdge> {
    private final ListenableGraph<String, AttributedEdge> innerGraph;

    public AttributedGraphHolder() {
        this.innerGraph = new DefaultListenableGraph<>(
                new SimpleDirectedWeightedGraph<>(AttributedEdge.class));
    }

    @Override
    public ListenableGraph<String, AttributedEdge> exposeInnerGraph() {
        return innerGraph;
    }

    @Override
    public JGraphXAdapter<String, AttributedEdge> getJgraphxRepresentation() {
        JGraphXAdapter<String, AttributedEdge> adapter = new JGraphXAdapter<>(innerGraph);
        applyEdgeStyles(adapter);
        return adapter;
    }

    private void applyEdgeStyles(JGraphXAdapter<String, AttributedEdge> adapter) {
        adapter.getEdgeToCellMap().forEach((edge, cell) -> {
            if (edge != null) {
                AttributedEdge attributedEdge = (AttributedEdge) edge;
                String style = mxConstants.STYLE_STROKECOLOR + "=" + attributedEdge.getColor() + ";";
                style += mxConstants.STYLE_STROKEWIDTH + "=" + attributedEdge.getPenWidth() + ";";

                //Dodaj etykiety wagi, jeśli waga jest określona
                if (!Double.isNaN(attributedEdge.getWeight())) {
                    style += mxConstants.STYLE_LABEL_POSITION + "=" + mxConstants.ALIGN_MIDDLE + ";";
                    style += mxConstants.STYLE_VERTICAL_LABEL_POSITION + "=" + mxConstants.ALIGN_MIDDLE + ";";
                    style += mxConstants.STYLE_FONTCOLOR + "=#000000;";
                    style += mxConstants.STYLE_FONTSIZE + "=15";
                    adapter.getModel().setValue(cell, String.valueOf(attributedEdge.getWeight()));
                }

                adapter.setCellStyle(style, new Object[]{cell});
            }
        });
    }
}