package com.project.housingservice.controller;

import com.project.housingservice.domain.response.Facility.AllFacilityResponse;
import com.project.housingservice.domain.storage.hibernate.Facility;
import com.project.housingservice.exception.HouseNotFoundException;
import com.project.housingservice.service.FacilityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("facility")
public class FacilityController {
    private FacilityService facilityService;

    @Autowired
    public void setFacilityService(FacilityService facilityService) {
        this.facilityService = facilityService;
    }

    @GetMapping(value = "{houseId}")
    public ResponseEntity<AllFacilityResponse> getAllFacilitiesByHouseId(@PathVariable Integer houseId) throws HouseNotFoundException {
        if (houseId < 1) { throw new RuntimeException("Invalid house ID."); }

        List<Facility> facilityList = facilityService.getAllFacilitiesByHouseId(houseId);
        if (facilityList.isEmpty()) {
            throw new HouseNotFoundException("The house with the id of " + houseId + " does not exist.");
        }

        return ResponseEntity.ok(AllFacilityResponse.builder()
                                                    .message("Returning all facilities with the house id of " + houseId)
                                                    .facilities(facilityList)
                                                    .build());
    }
}
