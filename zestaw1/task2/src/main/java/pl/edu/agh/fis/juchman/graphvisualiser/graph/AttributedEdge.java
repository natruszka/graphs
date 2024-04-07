package pl.edu.agh.fis.juchman.graphvisualiser.graph;

import org.jgrapht.graph.DefaultEdge;

public class AttributedEdge extends DefaultEdge {
    private String color = "grey";
    private float penWidth = 1.f;
    private double weight = 0.0;


    // Getters and setters
    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public float getPenWidth() {
        return penWidth;
    }
    public void setPenWidth(float penWidth){
        this.penWidth = penWidth;
    }

    public void setWeight(double weight){
        this.weight = weight;
    }
    public double getWeight() {
        return weight;
    }

}