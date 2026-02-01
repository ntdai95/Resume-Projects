package com.project.hr.domain.response.employee;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;

import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

public class PersonalDocument {
    @ApiModelProperty(notes = "The database generated PersonalDocument ID")
    private String id;
    @ApiModelProperty
    private String path;
    @ApiModelProperty
    private String title;
    @ApiModelProperty
    private String comment;
    @ApiModelProperty
    private Date createDate;
}
