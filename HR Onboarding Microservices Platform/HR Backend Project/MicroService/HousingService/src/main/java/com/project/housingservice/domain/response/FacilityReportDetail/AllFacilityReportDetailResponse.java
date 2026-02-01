package com.project.housingservice.domain.response.FacilityReportDetail;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.housingservice.domain.storage.hibernate.FacilityReportDetail;
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
