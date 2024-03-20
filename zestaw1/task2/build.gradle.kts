plugins {
    id("java")
}

group = "pl.edu.agh.fis.juchman"
version = "1.0"

repositories {
    mavenCentral()
    maven(url = "https://jitpack.io")/// for jgraphx
}
dependencies {
    implementation("org.jgrapht:jgrapht-core:1.5.2")
    implementation("org.jgrapht:jgrapht-ext:1.5.2")
    implementation("com.github.jgraph:jgraphx:v4.0.0")
    implementation("com.moandjiezana.toml:toml4j:0.7.2")
    implementation("com.google.guava:guava:33.1.0-jre")
    testImplementation(platform("org.junit:junit-bom:5.9.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.test {
    useJUnitPlatform()
}