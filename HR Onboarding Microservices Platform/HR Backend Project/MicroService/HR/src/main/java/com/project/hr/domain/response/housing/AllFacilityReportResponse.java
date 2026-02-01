package com.project.hr.domain.response.housing;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.hr.entity.FacilityReport;
import lombok.*;

import java.util.List;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AllFacilityReportResponse {
    private final boolean success = true;
    private String message;
    private List<FacilityReport> facilityReports;
}
