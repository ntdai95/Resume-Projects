package com.project.hr.domain.response.employee;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

public class Contact {
    @ApiModelProperty(notes = "The database generated Contact ID")
    private String id;
    @ApiModelProperty
    private String firstName;
    @ApiModelProperty
    private String lastName;
    @ApiModelProperty
    private String cellPhone;
    @ApiModelProperty
    private String alternatePhone;
    @ApiModelProperty
    private String email;
    @ApiModelProperty
    private String relationship;
    @ApiModelProperty
    private String type;

}
