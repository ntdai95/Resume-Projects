package com.project.onboard.domain.request.employee;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ContactRequest {

    private String firstName;
    private String lastName;
    private String cellPhone;
    private String alternatePhone;
    private String email;
    private String relationship;
    private String type;
}
