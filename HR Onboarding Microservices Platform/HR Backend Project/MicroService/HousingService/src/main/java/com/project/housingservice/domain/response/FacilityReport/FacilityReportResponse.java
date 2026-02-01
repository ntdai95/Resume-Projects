package com.project.housingservice.domain.response.FacilityReport;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.housingservice.domain.storage.hibernate.FacilityReport;
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
