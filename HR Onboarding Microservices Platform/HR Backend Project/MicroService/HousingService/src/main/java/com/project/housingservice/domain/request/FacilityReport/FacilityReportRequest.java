package com.project.housingservice.domain.request.FacilityReport;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class FacilityReportRequest {
    private Integer FacilityID;

    private String EmployeeID;

    private String Title;

    private String Description;
}
