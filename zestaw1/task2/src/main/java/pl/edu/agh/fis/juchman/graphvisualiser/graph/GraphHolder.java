package pl.edu.agh.fis.juchman.graphvisualiser.graph;

import org.jgrapht.ListenableGraph;
import org.jgrapht.ext.JGraphXAdapter;

public interface GraphHolder<V,E> {
    ListenableGraph<V, E> exposeInnerGraph();// The brains, you can modify the return value.
    JGraphXAdapter<V,E> getJgraphxRepresentation(); //The "not so clever sidekick", please please please, implement it to be a lazy accessor, and NOT cache it, synchronising it would no fun ugh... ALSO... DO... NOT.... MODIFY... THE RETURN VALUE IT IS READ ONLY

}
