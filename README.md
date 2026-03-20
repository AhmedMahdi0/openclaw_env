# OpenClaw Spring Boot Environment

A Spring Boot application for OpenClaw environment management.

## Project Structure

```
openclaw_env/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/com/example/openclaw/
│   │   │   ├── OpenclawEnvApplication.java
│   │   │   └── HelloController.java
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/com/example/openclaw/
└── README.md
```

## Technologies

- Java 21
- Spring Boot 3.4.3
- Maven 4.x

## Endpoints

- `GET /api/hello` - Welcome message
- `GET /api/health` - Health check

## Building and Running

### Build the project:
```bash
mvn clean package
```

### Run the application:
```bash
mvn spring-boot:run
```

Or run the generated JAR:
```bash
java -jar target/openclaw-env-1.0.0.jar
```

## Default Port

Application runs on port `8080`.

## API Examples

```bash
curl http://localhost:8080/api/hello
curl http://localhost:8080/api/health
```

## License

This project is part of the OpenClaw environment.