# Facial-Recognition-Attendance-System

## Project Description:
My vision for this project is to create a facial recognition system that can be used in schools, universitites, offices, and other places where attendance tracking is necessary. The system will use facial recognition technology to identify students or employees and record their attendance.

## Project Status ![Status](https://img.shields.io/badge/status-in%20progress-yellow)

## Features implemented thus far:
- Attendance recording for arrival and departure

## System requirements:
- Java
- Python
- Internet browser
- SQLite
- Maven
- Make
- CMake

## Installation
#### Linux
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r dependencies/requirements.txt

#### Windows
    python3 -m venv .venv
    .\.venv\Scripts\activate
    python.exe -m pip install --upgrade pip
    pip install -r dependencies/requirements.txt

## Compiling and testing:
1. Compile the project using: 
        
        mvn package
3. Run the tests using:
        
        make tests

## Running instructions:
1. Run the server using:
        
        make webapi

2. Run the frontend by visiting the url `http://localhost:7000/` on a browser

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Contributor

Nkosikhona Mlaba