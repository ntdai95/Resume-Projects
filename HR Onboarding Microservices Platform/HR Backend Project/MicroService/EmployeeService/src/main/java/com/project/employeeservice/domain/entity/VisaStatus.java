package com.project.employeeservice.domain.entity;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;

/**
 * @author Guohua Zhang
 * @create 2022-08-15 11:05 PM
 */
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

@Document
public class VisaStatus {
    @org.springframework.data.annotation.Id
    @ApiModelProperty(notes = "The database generated Contact ID")
    private String id;
    @ApiModelProperty
    private String visaType;
    @ApiModelProperty
    private Boolean activeFlag;
    @ApiModelProperty
    private Date startDate;
    @ApiModelProperty
    private Date endDate;
    @ApiModelProperty
    private Date lastModificationDate;
}
