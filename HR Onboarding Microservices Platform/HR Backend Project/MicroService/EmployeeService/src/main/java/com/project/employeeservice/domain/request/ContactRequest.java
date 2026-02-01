package com.project.employeeservice.domain.request;

import io.swagger.annotations.ApiModelProperty;
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
