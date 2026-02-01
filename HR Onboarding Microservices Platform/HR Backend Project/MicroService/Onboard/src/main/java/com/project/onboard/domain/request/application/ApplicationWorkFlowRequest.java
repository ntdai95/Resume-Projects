package com.project.onboard.domain.request.application;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ApplicationWorkFlowRequest {

    private String employeeID;

    private String createDate;

    private String lastModificationDate;

    private String status;

    private String comment;
}
