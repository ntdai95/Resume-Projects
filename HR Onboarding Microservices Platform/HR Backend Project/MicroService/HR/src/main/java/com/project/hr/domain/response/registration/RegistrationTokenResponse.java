package com.project.hr.domain.response.registration;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RegistrationTokenResponse {
    private Integer id;

    private String token;

    private String email;

    private String expirationDate;
}
