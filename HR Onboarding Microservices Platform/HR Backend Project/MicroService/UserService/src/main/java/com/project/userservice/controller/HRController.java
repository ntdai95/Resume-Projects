package com.project.userservice.controller;

import com.project.userservice.domain.entity.RegistrationTokenHibernate;
import com.project.userservice.domain.request.RegistrationToken;
import com.project.userservice.domain.response.RegistrationTokenResponse;
import com.project.userservice.exception.UserNotFoundException;
import com.project.userservice.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HRController {

    private final UserService userService;

    @Autowired
    public HRController(UserService userService) {
        this.userService = userService;
    }


    @PostMapping("/registrationToken")
    public RegistrationTokenResponse createToken(@RequestBody RegistrationToken request) throws UserNotFoundException {
        return userService.createRegistrationToken(request);
    }



}
