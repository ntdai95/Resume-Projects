package com.project.housingservice.domain.response.House;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.housingservice.domain.storage.hibernate.House;
import lombok.*;

import java.util.List;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AllHouseResponse {
    private final boolean success = true;
    private String message;
    private List<House> houses;
}