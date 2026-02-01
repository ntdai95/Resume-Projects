package com.project.hr.domain.request.registration;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class RegistrationToken {

    private String userEmail;

    private String expirationDate;

    private int createBy;

}
