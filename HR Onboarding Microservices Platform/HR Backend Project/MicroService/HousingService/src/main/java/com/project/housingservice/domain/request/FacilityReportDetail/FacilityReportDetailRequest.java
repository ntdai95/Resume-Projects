package com.project.housingservice.domain.request.FacilityReportDetail;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class FacilityReportDetailRequest {
    private Integer FacilityReportID;

    private String EmployeeID;

    private String Comment;
}
