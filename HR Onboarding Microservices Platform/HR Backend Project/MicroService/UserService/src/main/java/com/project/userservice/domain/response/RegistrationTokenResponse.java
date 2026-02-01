package com.project.userservice.domain.response;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class RegistrationTokenResponse {
    private Integer id;

    private String token;

    private String email;

    private String expirationDate;
}
