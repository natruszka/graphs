package pl.edu.agh.fis.juchman.graphvisualiser.configs;

import java.net.URI;

public record Config(SceneSetup sceneSetup, URI graphSourceUri, GraphSourceType graphSourceType, String lineElementSeparator) {
}
