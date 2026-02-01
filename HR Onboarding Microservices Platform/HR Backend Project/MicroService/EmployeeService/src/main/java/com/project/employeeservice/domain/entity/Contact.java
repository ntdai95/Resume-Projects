package com.project.employeeservice.domain.entity;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * @author Guohua Zhang
 * @create 2022-08-15 10:56 PM
 */
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

@Document
public class Contact {
    @Id
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
