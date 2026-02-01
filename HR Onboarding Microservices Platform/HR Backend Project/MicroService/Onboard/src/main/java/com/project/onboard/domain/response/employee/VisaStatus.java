package com.project.onboard.domain.response.employee;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;

import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

public class VisaStatus {
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
