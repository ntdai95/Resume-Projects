package com.project.applicationservice.domain.request;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ApplicationWorkFlowRequest {

    private int id;

    private String email;

    private String firstName;

    private String lastName;

    private String employeeID;

    private String createDate;

    private String lastModificationDate;

    private String status;

    private String comment;
}
