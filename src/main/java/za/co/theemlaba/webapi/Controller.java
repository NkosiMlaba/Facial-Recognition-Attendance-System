package za.co.theemlaba.webapi;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

import za.co.theemlaba.database.Database;

public class Controller {
    private final Database database;

    public Controller() {
        this.database = new Database("attendance.db");
    }

    public boolean enrollStudent(String firstName, String lastName, String email, String phoneNumber, String studentNumber, String course, int yearOfStudy, byte[] photoBytes) {
        if (photoBytes == null) return false;
        return database.insertStudent(firstName, lastName, email, phoneNumber, studentNumber, course, yearOfStudy, photoBytes);
    }

    public boolean enrollEmployee(String firstName, String lastName, String email, String phoneNumber, String position, String department, String startDate, String endDate, byte[] photoBytes) {
        if (photoBytes == null) return false;
        return database.insertEmployee(firstName, lastName, email, phoneNumber, position, department, startDate, endDate, photoBytes);
    }
}
