# Pet Paradise - Animal Store

A complete Spring Boot web application for a pet store with modern frontend and REST API.

## 🐾 Features

- **Modern Responsive Design** - Bootstrap 5 based UI
- **Pet Adoption Section** - Showcase available pets for adoption
- **Product Catalog** - Pet supplies and accessories
- **Service Information** - Veterinary, grooming, boarding services
- **Contact Form** - Customer communication
- **REST API** - Backend endpoints for future expansion
- **Mobile Friendly** - Fully responsive design

## 🏗️ Project Structure

```
pet-paradise-store/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/com/example/openclaw/
│   │   │   ├── OpenclawEnvApplication.java    # Main Spring Boot application
│   │   │   ├── HomeController.java            # Page controllers
│   │   │   └── HelloController.java           # REST API controllers
│   │   └── resources/
│   │       ├── static/
│   │       │   ├── css/styles.css             # Custom styles
│   │       │   └── js/app.js                  # Frontend JavaScript
│   │       ├── templates/
│   │       │   ├── index.html                 # Home page
│   │       │   └── about.html                 # About page
│   │       └── application.properties         # Configuration
│   └── test/
│       └── java/com/example/openclaw/
│           └── HelloControllerTest.java       # Unit tests
└── README.md
```

## 🛠️ Technologies

- **Backend:**
  - Java 21
  - Spring Boot 3.4.3
  - Spring Web MVC
  - Spring Thymeleaf
  - Maven 4.x

- **Frontend:**
  - HTML5, CSS3, JavaScript (ES6+)
  - Bootstrap 5.3
  - Font Awesome 6.4
  - Responsive Design

## 🚀 Getting Started

### Prerequisites
- Java 21 or later
- Maven 3.6+

### Build the Project
```bash
mvn clean package
```

### Run the Application
```bash
mvn spring-boot:run
```

Or run the generated JAR:
```bash
java -jar target/openclaw-env-1.0.0.jar
```

### Development Mode
```bash
mvn spring-boot:run -Dspring-boot.run.arguments=--server.port=8081
```

## 🌐 Application Access

- **Home Page:** http://localhost:8080/
- **About Page:** http://localhost:8080/about
- **API Health:** http://localhost:8080/api/health
- **API Hello:** http://localhost:8080/api/hello

## 📱 Pages & Features

### Home Page (`/`)
- Hero section with call-to-action
- Available pets gallery
- Product showcase
- Services overview
- Contact form

### About Page (`/about`)
- Company story
- Team members
- Core values
- Statistics

### REST API Endpoints
- `GET /api/hello` - Welcome message
- `GET /api/health` - Health check with status
- `GET /api/pets` - Pet listing (placeholder)
- `GET /api/products` - Product listing (placeholder)

## 🎨 Frontend Features

- **Responsive Navigation** - Collapsible navbar
- **Interactive Cards** - Hover effects and animations
- **Form Validation** - Client-side validation
- **Cart Functionality** - Local storage based cart
- **Notifications** - Toast notifications
- **API Integration** - JavaScript fetch API

## 🧪 Testing

Run unit tests:
```bash
mvn test
```

## 🔧 Configuration

Edit `src/main/resources/application.properties`:
```properties
server.port=8080
spring.application.name=pet-paradise-store
spring.thymeleaf.cache=false  # Disable cache for development
```

## 📦 Deployment

### Create Executable JAR
```bash
mvn clean package -DskipTests
```

### Run with Custom Port
```bash
java -jar target/openclaw-env-1.0.0.jar --server.port=8081
```

## 🔄 Future Enhancements

1. **Database Integration** - PostgreSQL/MySQL for pets and products
2. **User Authentication** - Spring Security for admin panel
3. **E-commerce Features** - Checkout, payments, orders
4. **Admin Dashboard** - Manage pets, products, orders
5. **Image Upload** - Cloud storage for pet photos
6. **Search & Filters** - Advanced pet/product search
7. **Reviews & Ratings** - Customer feedback system

## 📄 License

This project is developed as a demonstration of Spring Boot full-stack development.

---

**Pet Paradise** - Your trusted partner for all pet needs since 2010 🐕🐈🐦