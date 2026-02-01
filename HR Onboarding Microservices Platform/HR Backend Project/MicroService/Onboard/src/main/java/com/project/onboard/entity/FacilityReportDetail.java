package com.project.onboard.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class FacilityReportDetail {
    private Integer id;

    private FacilityReport facilityReport;

    private String employeeID;

    private String comment;

    private String createDate;

    private String lastModificationDate;
}
