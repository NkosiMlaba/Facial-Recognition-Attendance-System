package za.co.theemlaba.webapi;

import io.javalin.Javalin;
import io.javalin.http.UploadedFile;
import io.javalin.http.staticfiles.Location;
import io.javalin.rendering.template.JavalinThymeleaf;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class WebServer {
    private static final Logger logger = LoggerFactory.getLogger(WebServer.class);
    private static Controller controller = new Controller();
    

    public static void main(String[] args) {
        
        Javalin app = startServer();
        

        app.before(WebServer::logRequest);
        app.after(WebServer::logResponse);

        app.get("/", ctx -> ctx.render("index.html"));
        app.get("/arrival", ctx -> ctx.render("arrival.html"));
        app.get("/departure", ctx -> ctx.render("departure.html"));

        app.get("/enroll-student", ctx -> ctx.render("student_enroll.html"));
        app.get("/enroll-employee", ctx -> ctx.render("employee_enroll.html"));

        app.post("/enroll-student", ctx -> {
            String firstName = ctx.formParam("firstName");
            String lastName = ctx.formParam("lastName");
            String email = ctx.formParam("email");
            String phoneNumber = ctx.formParam("phoneNumber");
            String studentNumber = ctx.formParam("studentNumber");
            String course = ctx.formParam("course");
            int yearOfStudy = Integer.parseInt(ctx.formParam("yearOfStudy"));
            String photoData = ctx.formParam("photoData");

            if (photoData != null && !photoData.isEmpty()) {
                try {
                    byte[] photoBytes = java.util.Base64.getDecoder().decode(photoData.split(",")[1]);
                    boolean success = controller.enrollStudent(firstName, lastName, email, phoneNumber, studentNumber, course, yearOfStudy, photoBytes);
        
                    if (success) {
                        ctx.result("Student enrolled successfully!");
                    } else {
                        ctx.result("Failed to enroll student.");
                    }
                } catch (Exception e) {
                    logger.error("Error processing photo data: " + e.getMessage(), e);
                    ctx.result("Failed to process photo.");
                }
            } else {
                ctx.result("No photo captured.");
            }
        });

        app.post("/enroll-employee", ctx -> {
            String firstName = ctx.formParam("firstName");
            String lastName = ctx.formParam("lastName");
            String email = ctx.formParam("email");
            String phoneNumber = ctx.formParam("phoneNumber");
            String position = ctx.formParam("position");
            String department = ctx.formParam("department");
            String startDate = ctx.formParam("startDate");
            String endDate = ctx.formParam("endDate");
            String photoData = ctx.formParam("photoData");

            if (photoData != null && !photoData.isEmpty()) {
                try {
                    byte[] photoBytes = java.util.Base64.getDecoder().decode(photoData.split(",")[1]);
                    boolean success = controller.enrollEmployee(firstName, lastName, email, phoneNumber, position, department, startDate, endDate, photoBytes);

                    if (success) {
                        ctx.result("Employee enrolled successfully!");
                    } else {
                        ctx.result("Failed to enroll employee.");
                    }
                } catch (Exception e) {
                    logger.error("Error processing photo data: " + e.getMessage(), e);
                    ctx.result("Failed to process photo.");
                }
            } else {
                ctx.result("No photo uploaded.");
            }
        });
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
        templateResolver.setPrefix("static/templates/");
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
