package com.project.housingservice.controller;

import com.project.housingservice.domain.request.FacilityReportDetail.FacilityReportDetailRequest;
import com.project.housingservice.domain.response.FacilityReportDetail.AllFacilityReportDetailResponse;
import com.project.housingservice.domain.response.FacilityReportDetail.FacilityReportDetailResponse;
import com.project.housingservice.domain.storage.hibernate.FacilityReportDetail;
import com.project.housingservice.exception.FacilityReportDetailNotFoundException;
import com.project.housingservice.exception.FacilityReportNotFoundException;
import com.project.housingservice.service.FacilityReportDetailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("facilityReportDetail")
public class FacilityReportDetailController {
    private FacilityReportDetailService facilityReportDetailService;

    @Autowired
    public void setFacilityReportDetailService(FacilityReportDetailService facilityReportDetailService) {
        this.facilityReportDetailService = facilityReportDetailService;
    }

    @GetMapping(value = "/{facilityReportId}")
    public ResponseEntity<AllFacilityReportDetailResponse> getAllFacilityReportDetailByFacilityReportId(@PathVariable Integer facilityReportId) throws FacilityReportDetailNotFoundException {
        if (facilityReportId < 1) {
            throw new RuntimeException("Invalid facility report ID.");
        }

        List<FacilityReportDetail> facilityReportDetailList = facilityReportDetailService.getAllFacilityReportDetailByFacilityReportId(facilityReportId);
        if (facilityReportDetailList.size() == 0) {
            throw new FacilityReportDetailNotFoundException("No facility report detail with the facility report id of " + facilityReportId + " exists in the database.");
        }

        return ResponseEntity.ok(AllFacilityReportDetailResponse.builder()
                                                                .message("Returning all facility report details")
                                                                .facilityReportDetails(facilityReportDetailList)
                                                                .build());
    }

    @PostMapping
    public ResponseEntity<FacilityReportDetailResponse> createNewFacilityReportDetail(@RequestBody FacilityReportDetailRequest facilityReportDetailRequest) throws FacilityReportNotFoundException {
        int facilityReportDetailID = facilityReportDetailService.createNewFacilityReportDetail(facilityReportDetailRequest);
        if (facilityReportDetailID == -1) {
            throw new FacilityReportNotFoundException("The facility report with the id of " + facilityReportDetailRequest.getFacilityReportID() + " does not exist.");
        }

        return ResponseEntity.ok(FacilityReportDetailResponse.builder()
                                                             .message("New facility report detail with the id of " + facilityReportDetailID + " has been created.")
                                                             .build());
    }

    @PatchMapping(value = "/{facilityReportDetailID}")
    public ResponseEntity<FacilityReportDetailResponse> updateFacilityReportDetail(@PathVariable Integer facilityReportDetailID,
                                                                                   @RequestParam String employeeID, @RequestParam String newComment) throws FacilityReportDetailNotFoundException {
        if (facilityReportDetailID < 1) {
            throw new RuntimeException("Invalid facility report detail ID.");
        }

        boolean isFacilityReportDetailExist = facilityReportDetailService.updateFacilityReportDetail(facilityReportDetailID, employeeID, newComment);
        if (!isFacilityReportDetailExist) {
            throw new FacilityReportDetailNotFoundException("The facility report detail with the id of " + facilityReportDetailID + " does not exist or you did not created this facility report detail.");
        }

        return ResponseEntity.ok(FacilityReportDetailResponse.builder()
                                                             .message("Facility Report Detail with the id of " + facilityReportDetailID + " has been updated.")
                                                             .build());
    }
}
