package pl.edu.agh.fis.juchman.graphvisualiser.input;

import pl.edu.agh.fis.juchman.graphvisualiser.GraphHolder;

public interface GraphSource<V,E> {
    GraphHolder<V,E> getGraph();
}
