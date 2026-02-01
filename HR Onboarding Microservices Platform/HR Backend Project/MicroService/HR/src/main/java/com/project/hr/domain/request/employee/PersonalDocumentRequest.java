package com.project.hr.domain.request.employee;

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
