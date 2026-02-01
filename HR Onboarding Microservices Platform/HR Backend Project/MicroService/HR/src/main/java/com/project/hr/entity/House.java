package com.project.hr.entity;

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
public class House {
    private Integer id;

    private Landlord landlord;

    private String address;

    private Integer maxOccupant;

    private Integer currentEmployeeCount;

    private List<Facility> facilities;
}
