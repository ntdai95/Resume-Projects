package com.project.onboard.domain.response.employee;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

public class Address {
    @ApiModelProperty(notes = "The database generated Contact ID")
    private String id;
    @ApiModelProperty
    private String addressLine1;
    @ApiModelProperty
    private String addressLine2;
    @ApiModelProperty
    private String city;
    @ApiModelProperty
    private String state;
    @ApiModelProperty
    private String zipCode;
}
