package za.co.theemlaba.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.File;

public class AttendanceDatabase {
    private String URL;
    private static final String DATABASE_DIR = "src/main/resources/database";

    public AttendanceDatabase(String URL) {
        setDatabaseName(URL);
    }

    public void setDatabaseName(String databaseName) {
        createDatabaseDirectory();
        this.URL = "jdbc:sqlite:" + DATABASE_DIR + File.separator + databaseName;
        initialiseDatabase();
    }

    private void createDatabaseDirectory() {
        File directory = new File(DATABASE_DIR);
        if (!directory.exists()) {
            if (directory.mkdirs()) {
                System.out.println("Database directory created.");
            } else {
                System.out.println("Failed to create database directory.");
            }
        }
    }

    public void initialiseDatabase() {
        String userTableSQL = """
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE,
                    name TEXT,
                    role TEXT,
                    photo_path TEXT
                );
                """;
        try (Connection conn = DriverManager.getConnection(URL);
             PreparedStatement pstmt = conn.prepareStatement(userTableSQL)) {
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("Error initializing database: " + e.getMessage());
        }
    }

    public boolean insertStudent(String firstName, String lastName, String email, String phoneNumber, String studentNumber, String course, int yearOfStudy, byte[] photo) {
        try (Connection conn = DriverManager.getConnection(URL)) {
            conn.setAutoCommit(false);

            // Insert into Users table
            String insertUserSql = """
                INSERT INTO Users (user_type, first_name, last_name, email, phone_number)
                VALUES ('Student', ?, ?, ?, ?)
            """;
            try (PreparedStatement pstmt = conn.prepareStatement(insertUserSql, Statement.RETURN_GENERATED_KEYS)) {
                pstmt.setString(1, firstName);
                pstmt.setString(2, lastName);
                pstmt.setString(3, email);
                pstmt.setString(4, phoneNumber);
                pstmt.executeUpdate();

                ResultSet keys = pstmt.getGeneratedKeys();
                if (keys.next()) {
                    int userId = keys.getInt(1);

                    // Insert into Student table
                    String insertStudentSql = """
                        INSERT INTO Student (student_id, student_number, course, year_of_study)
                        VALUES (?, ?, ?, ?)
                    """;
                    try (PreparedStatement studentStmt = conn.prepareStatement(insertStudentSql)) {
                        studentStmt.setInt(1, userId);
                        studentStmt.setString(2, studentNumber);
                        studentStmt.setString(3, course);
                        studentStmt.setInt(4, yearOfStudy);
                        studentStmt.executeUpdate();
                    }

                    // Insert photo into User_Photos table
                    String insertPhotoSql = """
                        INSERT INTO User_Photos (user_id, photo)
                        VALUES (?, ?)
                    """;
                    try (PreparedStatement photoStmt = conn.prepareStatement(insertPhotoSql)) {
                        photoStmt.setInt(1, userId);
                        photoStmt.setBytes(2, photo);
                        photoStmt.executeUpdate();
                    }

                    conn.commit();
                    return true;
                }
            }
        } catch (SQLException e) {
            System.err.println("Error inserting student: " + e.getMessage());
        }
        return false;
    }

    public boolean insertEmployee(String firstName, String lastName, String email, String phoneNumber, String position, String department, String startDate, String endDate, byte[] photo) {
        try (Connection conn = DriverManager.getConnection(URL)) {
            conn.setAutoCommit(false);

            // Insert into Users table
            String insertUserSql = """
                INSERT INTO Users (user_type, first_name, last_name, email, phone_number)
                VALUES ('Employee', ?, ?, ?, ?)
            """;
            try (PreparedStatement pstmt = conn.prepareStatement(insertUserSql, Statement.RETURN_GENERATED_KEYS)) {
                pstmt.setString(1, firstName);
                pstmt.setString(2, lastName);
                pstmt.setString(3, email);
                pstmt.setString(4, phoneNumber);
                pstmt.executeUpdate();

                ResultSet keys = pstmt.getGeneratedKeys();
                if (keys.next()) {
                    int userId = keys.getInt(1);

                    // Insert into Employee table
                    String insertEmployeeSql = """
                        INSERT INTO Employee (employee_id, position, department, start_date, end_date)
                        VALUES (?, ?, ?, ?, ?)
                    """;
                    try (PreparedStatement employeeStmt = conn.prepareStatement(insertEmployeeSql)) {
                        employeeStmt.setInt(1, userId);
                        employeeStmt.setString(2, position);
                        employeeStmt.setString(3, department);
                        employeeStmt.setString(4, startDate);
                        employeeStmt.setString(5, endDate);
                        employeeStmt.executeUpdate();
                    }

                    // Insert photo into User_Photos table
                    String insertPhotoSql = """
                        INSERT INTO User_Photos (user_id, photo)
                        VALUES (?, ?)
                    """;
                    try (PreparedStatement photoStmt = conn.prepareStatement(insertPhotoSql)) {
                        photoStmt.setInt(1, userId);
                        photoStmt.setBytes(2, photo);
                        photoStmt.executeUpdate();
                    }

                    conn.commit();
                    return true;
                }
            }
        } catch (SQLException e) {
            System.err.println("Error inserting employee: " + e.getMessage());
        }
        return false;
    }
}
