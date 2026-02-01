package com.project.hr.domain.response.employee;

import lombok.*;

import java.util.Date;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class EmployeeVisaInfo {
    private String employeeId;
    private String name;
    private String workAuthorization;
    private Date expirationDate;
    private int dateLeft;
}
