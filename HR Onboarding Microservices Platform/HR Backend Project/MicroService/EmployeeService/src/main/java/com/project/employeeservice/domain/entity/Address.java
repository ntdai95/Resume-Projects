package com.project.employeeservice.domain.entity;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * @author Guohua Zhang
 * @create 2022-08-15 11:00 PM
 */
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

@Document
public class Address {
    @org.springframework.data.annotation.Id
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
