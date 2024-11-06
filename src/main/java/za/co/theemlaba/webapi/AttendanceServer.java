package za.co.theemlaba.webapi;

import io.javalin.Javalin;
import io.javalin.http.Context;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.apache.log4j.chainsaw.Main;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import io.javalin.Javalin;
import io.javalin.http.staticfiles.Location;
import io.javalin.rendering.template.JavalinThymeleaf;
import io.javalin.http.Context;
import org.apache.log4j.chainsaw.Main;
import java.util.Scanner;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;



public class AttendanceServer {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    public static void main(String[] args) {
        Javalin app = startServer(args);

        app.before(AttendanceServer::logRequest);
        app.after(AttendanceServer::logResponse);

        app.get("/", ctx -> ctx.result("Welcome to the Attendance Dashboard"));
        app.get("/start-recognition", AttendanceServer::triggerFaceRecognition);

        app.get("/start", ctx -> {
            ctx.render("index.html"); // Ensure this path is correct
        });
    }

    public static Javalin startServer(String[] args) {
        Javalin app = Javalin.create(config -> {
            config.bundledPlugins.enableCors(cors -> cors.addRule(it -> it.anyHost()));

            config.staticFiles.add(staticFileConfig -> {
                staticFileConfig.directory = "src/main/resources/static";
                staticFileConfig.location = Location.EXTERNAL;
            });

            config.fileRenderer(new JavalinThymeleaf(buildTemplateEngine()));
        });

        return app.start(7000);
    }

    public static TemplateEngine buildTemplateEngine() {
        ClassLoaderTemplateResolver templateResolver = new ClassLoaderTemplateResolver();
        templateResolver.setPrefix("templates/");
        templateResolver.setSuffix(".html");
        templateResolver.setTemplateMode("HTML");
        templateResolver.setCharacterEncoding("UTF-8");
        TemplateEngine templateEngine = new TemplateEngine();
        templateEngine.setTemplateResolver(templateResolver);
        return templateEngine;
    }

    private static void triggerFaceRecognition(Context ctx) {
        try {
            URL url = new URL("http://localhost:5001/start-recognition");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            int responseCode = connection.getResponseCode();

            if (responseCode == 200) {
                ctx.result("Face recognition started successfully.");
            } else {
                ctx.result("Failed to start face recognition.");
            }

        } catch (IOException e) {
            ctx.result("Error connecting to Python API: " + e.getMessage());
        }
    }

    public static void logRequest(Context ctx) {
        logger.info("Received {} request to {}", ctx.method(), ctx.url().toString());
    }

    public static void logResponse(Context ctx) {
        logger.info("Responded with status {}", ctx.status());
    }
    
}
