package pl.edu.agh.fis.juchman.graphvisualiser.display;
import com.mxgraph.layout.mxCircleLayout;
import com.mxgraph.swing.mxGraphComponent;
import com.mxgraph.model.mxGraphModel;
import com.mxgraph.util.mxConstants;
import com.mxgraph.util.mxStyleUtils;
import org.jgrapht.ext.JGraphXAdapter;
import org.jgrapht.graph.DefaultEdge;
import java.util.Collection;
import pl.edu.agh.fis.juchman.graphvisualiser.GraphHolder;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.SceneSetup;

import javax.swing.*;
import java.awt.*;

public class GraphDisplay extends JFrame {

    private static  Dimension frameSize;
    private static int radius;
    private static boolean displayAsDirectedGraph = false;


    public GraphDisplay(SceneSetup sceneSetup) throws HeadlessException {
        super(sceneSetup.title());
    }

    private void load(GraphHolder<String, DefaultEdge> graph){

        JGraphXAdapter<String, DefaultEdge> jgxAdapter = graph.getJgraphxRepresentation();
        setPreferredSize(frameSize);
        mxGraphComponent component = new mxGraphComponent(jgxAdapter);

        if(!displayAsDirectedGraph){
            mxGraphModel graphModel  = (mxGraphModel)component.getGraph().getModel();
            Collection<Object> cells =  graphModel.getCells().values();
            mxStyleUtils.setCellStyles(component.getGraph().getModel(), cells.toArray(), mxConstants.STYLE_ENDARROW, mxConstants.NONE); // Disable arrows
            for (Object cell : cells) {
                if (component.getGraph().getModel().isEdge(cell)) {
                    mxStyleUtils.setCellStyles(component.getGraph().getModel(), new Object[]{cell}, mxConstants.STYLE_NOLABEL, "1"); /// Disable edge labels
                }
            }
        }
        getContentPane().add(component);
        component.setConnectable(false);
        component.getGraph().setAllowDanglingEdges(false);
        mxCircleLayout layout = new mxCircleLayout(jgxAdapter);

        // center the circle
        layout.setX0((frameSize.width / 2.0) - radius);
        layout.setY0((frameSize.height / 2.0) - radius);
        layout.setRadius(radius);
        layout.setMoveCircle(true);
        layout.execute(jgxAdapter.getDefaultParent());
    }
    public static void display(SceneSetup sceneSetup, GraphHolder<String,DefaultEdge> graphHolder) {
        GraphDisplay.frameSize =  new Dimension(sceneSetup.width(), sceneSetup.height());
        GraphDisplay.radius = sceneSetup.radius();
        GraphDisplay.displayAsDirectedGraph = sceneSetup.displayAsDirectedGraph();


        GraphDisplay frame = new GraphDisplay(sceneSetup);
        frame.load(graphHolder);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(sceneSetup.width(), sceneSetup.height());
        frame.setVisible(true);
    }
}
