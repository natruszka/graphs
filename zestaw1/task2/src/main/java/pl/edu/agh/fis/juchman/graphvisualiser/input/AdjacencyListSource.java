package pl.edu.agh.fis.juchman.graphvisualiser.input;

import com.google.common.io.Files;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.util.SupplierUtil;
import pl.edu.agh.fis.juchman.graphvisualiser.graph.GraphHolder;
import pl.edu.agh.fis.juchman.graphvisualiser.graph.SimpleGraphHolder;
import pl.edu.agh.fis.juchman.graphvisualiser.configs.Config;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.IntStream;

class AdjacencyListSource implements GraphSource<String, DefaultEdge>{

    private final Config config;
    private final SimpleGraphHolder<String,DefaultEdge> graphHolder;
    public AdjacencyListSource(Config config) {
        this.config = config;
        this.graphHolder = new SimpleGraphHolder<>(SupplierUtil.createStringSupplier(),SupplierUtil.createDefaultEdgeSupplier());
    }

    @Override
    public GraphHolder<String,DefaultEdge> getGraph() { // God, that looks compact... but still, of course I didn't implement validity checking :)))
        try {
            List<String> lines = Files.readLines(Path.of(config.graphSourceUri()).toFile(), Charset.defaultCharset());
            IntStream.range(1,lines.size()+1).forEach(val -> graphHolder.exposeInnerGraph().addVertex(String.valueOf(val)));
            for(var str : lines){
                String[] line = str.split("\\.");
                for(var el : line[1].trim().split(config.lineElementSeparator())){
                    graphHolder.exposeInnerGraph().addEdge(line[0],el);
                }
            }
            return graphHolder;
        }catch(IOException ioException){throw new RuntimeException(ioException);}
    }
}
