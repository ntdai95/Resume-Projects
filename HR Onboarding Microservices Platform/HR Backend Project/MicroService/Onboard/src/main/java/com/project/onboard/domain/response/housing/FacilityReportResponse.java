package com.project.onboard.domain.response.housing;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.onboard.entity.FacilityReport;
import lombok.*;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class FacilityReportResponse {
    private final boolean success = true;
    private String message;
    private FacilityReport facilityReport;
}
