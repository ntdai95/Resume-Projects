package com.project.userservice.controller;

import com.project.userservice.domain.request.RegisterUserRequest;
import com.project.userservice.domain.response.RegisterUserResponse;
import com.project.userservice.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class UserController {

    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/register")
    public RegisterUserResponse registerUser(@RequestBody RegisterUserRequest request, @RequestParam String token) {
        int userId = userService.registerUser(request, token);
        return RegisterUserResponse.builder().message("User created, userId: " + userId).build();
    }
}
