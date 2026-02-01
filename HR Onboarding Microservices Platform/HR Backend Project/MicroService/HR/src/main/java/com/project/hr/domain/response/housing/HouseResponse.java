package com.project.hr.domain.response.housing;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.project.hr.entity.House;
import lombok.*;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class HouseResponse {
    private final boolean success = true;
    private String message;
    private House house;
}
