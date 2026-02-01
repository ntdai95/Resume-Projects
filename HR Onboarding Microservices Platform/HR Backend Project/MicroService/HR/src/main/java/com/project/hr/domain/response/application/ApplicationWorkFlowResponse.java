package com.project.hr.domain.response.application;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ApplicationWorkFlowResponse {

    private int id;

    private String employeeID;

    private String createDate;

    private String lastModificationDate;

    private String status;

    private String comment;
}
