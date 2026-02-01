package com.project.onboard.domain.request.housing;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class HouseRequest {
    private int LandlordID;

    private String Address;

    private Integer MaxOccupant;
}
