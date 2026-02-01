package com.project.onboard.domain.response.housing;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.onboard.entity.FacilityReportDetail;
import lombok.*;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class FacilityReportDetailResponse {
    private final boolean success = true;
    private String message;
    private FacilityReportDetail facilityReportDetail;
}
