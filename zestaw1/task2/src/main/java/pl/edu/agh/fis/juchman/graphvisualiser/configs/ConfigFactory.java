package pl.edu.agh.fis.juchman.graphvisualiser.configs;

import com.moandjiezana.toml.Toml;

import java.net.URI;
import java.nio.file.Path;

public final class ConfigFactory { /// Returns Config based on data in TOML, the input is path
    public static Config createConfig(URI configurationFileURI){
        Toml configSource = new Toml().read(Path.of(configurationFileURI).toFile());
        SceneSetup sceneSetup = new SceneSetup(configSource.getString("Config.SceneSetup.title"), configSource.getLong("Config.SceneSetup.width").intValue(), configSource.getLong("Config.SceneSetup.height").intValue(),configSource.getLong("Config.SceneSetup.radius").intValue(),configSource.getBoolean("Config.SceneSetup.displayAsDirectedGraph"));
        return new Config(sceneSetup,URI.create(configSource.getString("Config.graphSourceUri")),GraphSourceType.valueOf(configSource.getString("Config.graphSourceType")),configSource.getString("Config.lineElementSeparator"));
    }
}
