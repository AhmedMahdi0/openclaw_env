package com.example.openclaw;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Welcome to Pet Paradise Store API!";
    }
    
    @GetMapping("/health")
    public Map<String, String> health() {
        Map<String, String> status = new HashMap<>();
        status.put("status", "UP");
        status.put("service", "pet-paradise-store");
        status.put("version", "1.0.0");
        return status;
    }
    
    @GetMapping("/pets")
    public Map<String, Object> getPets() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Pet listing endpoint");
        response.put("endpoint", "/api/pets");
        response.put("description", "This endpoint will return available pets from the store");
        return response;
    }
    
    @GetMapping("/products")
    public Map<String, Object> getProducts() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Product listing endpoint");
        response.put("endpoint", "/api/products");
        response.put("description", "This endpoint will return pet products from the store");
        return response;
    }
}