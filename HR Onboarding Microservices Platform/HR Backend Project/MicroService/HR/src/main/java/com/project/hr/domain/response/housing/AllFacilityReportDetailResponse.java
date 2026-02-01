package com.project.hr.domain.response.housing;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.hr.entity.FacilityReportDetail;
import lombok.*;

import java.util.List;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AllFacilityReportDetailResponse {
    private final boolean success = true;
    private String message;
    private List<FacilityReportDetail> facilityReportDetails;
}
