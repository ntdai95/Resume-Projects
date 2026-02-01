package com.project.onboard.entity;

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
public class Facility {
    private Integer id;

    private House house;

    private String type;

    private String description;

    private Integer quantity;

    private List<FacilityReport> facilityReports;
}
