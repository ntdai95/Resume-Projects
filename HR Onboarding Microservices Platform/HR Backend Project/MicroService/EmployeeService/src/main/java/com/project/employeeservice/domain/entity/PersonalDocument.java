package com.project.employeeservice.domain.entity;

import io.swagger.annotations.ApiModelProperty;
import org.springframework.data.annotation.Id;
import lombok.*;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;

/**
 * @author Guohua Zhang
 * @create 2022-08-15 11:08 PM
 */
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

@Document
public class PersonalDocument {
    @Id
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
