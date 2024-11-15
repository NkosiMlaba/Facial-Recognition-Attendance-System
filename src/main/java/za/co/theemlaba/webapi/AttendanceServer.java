package za.co.theemlaba.webapi;

import io.javalin.Javalin;
import io.javalin.http.staticfiles.Location;
import io.javalin.rendering.template.JavalinThymeleaf;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AttendanceServer {
    private static final Logger logger = LoggerFactory.getLogger(AttendanceServer.class);

    public static void main(String[] args) {
        Javalin app = startServer();

        app.before(AttendanceServer::logRequest);
        app.after(AttendanceServer::logResponse);

        app.get("/", ctx -> ctx.render("index.html"));
        app.get("/arrival", ctx -> ctx.render("arrival.html"));
        app.get("/departure", ctx -> ctx.render("departure.html"));
    }

    public static Javalin startServer() {
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

    public static void logRequest(io.javalin.http.Context ctx) {
        logger.info("Received {} request to {}", ctx.method(), ctx.url());
    }

    public static void logResponse(io.javalin.http.Context ctx) {
        logger.info("Responded with status {}", ctx.status());
    }
}
