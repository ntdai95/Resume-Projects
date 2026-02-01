package com.project.employeeservice.domain.request;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;

import java.util.Date;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class PersonalDocumentRequest {
    private String path;
    private String title;
    private String comment;
    private Date createDate;
}
