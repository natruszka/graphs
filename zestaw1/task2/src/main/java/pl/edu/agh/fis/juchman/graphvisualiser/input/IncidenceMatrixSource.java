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
import java.util.Stack;
import java.util.stream.IntStream;

class IncidenceMatrixSource implements GraphSource<String, DefaultEdge> {

    private final Config config;
    private final SimpleGraphHolder<String,DefaultEdge> graphHolder;
    public IncidenceMatrixSource(Config config) {
        this.config = config;
        this.graphHolder = new SimpleGraphHolder<>(SupplierUtil.createStringSupplier(),SupplierUtil.createDefaultEdgeSupplier());
    }

    @Override
    public GraphHolder<String, DefaultEdge> getGraph() {
        try { // I really do not like these checked expressions.
            List<String[]> lines = Files.readLines(Path.of(config.graphSourceUri()).toFile(), Charset.defaultCharset()).stream().map(line -> line.split(config.lineElementSeparator())).toList();
            IntStream.range(0,lines.size()).forEach(val -> graphHolder.exposeInnerGraph().addVertex(String.valueOf(val)));
            Stack<Integer> stack = new Stack<>();
            int noOfLines = lines.size();
            for(int j=0; j<lines.get(0).length; ++j){ /// should be true as long as the file well-formed
                for(int i=0; i<noOfLines;++i){
                    if(stack.empty() && lines.get(i)[j].equals("1")){
                        stack.push(i);
                    }else if(lines.get(i)[j].equals("1")){
                        graphHolder.exposeInnerGraph().addEdge(String.valueOf(i),String.valueOf(stack.pop()));
                    }
                }
            }
        }catch(IOException ioException){
            throw new RuntimeException(ioException);// It works... Please don't judge.
        }
        return graphHolder;
    }
}
