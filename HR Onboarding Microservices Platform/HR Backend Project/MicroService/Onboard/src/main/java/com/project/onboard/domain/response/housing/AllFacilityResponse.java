package com.project.onboard.domain.response.housing;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.onboard.entity.Facility;
import lombok.*;

import java.util.List;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AllFacilityResponse {
    private final boolean success = true;
    private String message;
    private List<Facility> facilities;
}
