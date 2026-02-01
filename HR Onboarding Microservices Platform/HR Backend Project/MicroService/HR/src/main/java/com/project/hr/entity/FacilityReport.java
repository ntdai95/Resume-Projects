package com.project.hr.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;

import java.util.List;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class FacilityReport {
    private Integer id;

    private Facility facility;

    private String employeeID;

    private String title;

    private String description;

    private String createDate;

    private String status;

    private List<FacilityReportDetail> facilityReportDetails;
}
