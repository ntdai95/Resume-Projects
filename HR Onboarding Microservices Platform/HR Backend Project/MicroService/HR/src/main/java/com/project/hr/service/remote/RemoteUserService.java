package com.project.hr.service.remote;

import com.project.hr.domain.request.registration.RegistrationToken;
import com.project.hr.domain.response.registration.RegistrationTokenResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient("user")
public interface RemoteUserService {

    @PostMapping("user/registrationToken")
    RegistrationTokenResponse createToken(@RequestBody RegistrationToken request);
}
