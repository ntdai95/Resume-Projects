package com.project.employeeservice.domain.request;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class AddressRequest {

    private String addressLine1;
    private String addressLine2;
    private String city;
    private String state;
    private String zipCode;
}
