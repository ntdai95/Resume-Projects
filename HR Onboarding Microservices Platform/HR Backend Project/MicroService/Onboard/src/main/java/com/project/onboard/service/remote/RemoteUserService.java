package com.project.onboard.service.remote;

import com.project.onboard.domain.request.user.RegisterUserRequest;
import com.project.onboard.domain.response.user.RegisterUserResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient("user")
public interface RemoteUserService {

    @PostMapping("user/register")
    RegisterUserResponse registerUser(@RequestBody RegisterUserRequest request, @RequestParam String token);
}
