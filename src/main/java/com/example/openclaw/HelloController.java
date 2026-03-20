package com.example.openclaw;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello from OpenClaw Spring Boot Application!";
    }
    
    @GetMapping("/health")
    public String health() {
        return "{\"status\": \"UP\", \"service\": \"openclaw-env\"}";
    }
}