package com.project.housingservice.controller;

import com.project.housingservice.domain.request.FacilityReport.FacilityReportRequest;
import com.project.housingservice.domain.response.FacilityReport.AllFacilityReportResponse;
import com.project.housingservice.domain.response.FacilityReport.FacilityReportResponse;
import com.project.housingservice.domain.storage.hibernate.FacilityReport;
import com.project.housingservice.exception.FacilityNotFoundException;
import com.project.housingservice.exception.FacilityReportNotFoundException;
import com.project.housingservice.service.FacilityReportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("facilityReport")
public class FacilityReportController {
    private FacilityReportService facilityReportService;

    @Autowired
    public void setFacilityReportService(FacilityReportService facilityReportService) {
        this.facilityReportService = facilityReportService;
    }

    @PostMapping
    public ResponseEntity<FacilityReportResponse> createNewFacilityReport(@RequestBody FacilityReportRequest facilityReportRequest) throws FacilityNotFoundException {
        int facilityReportID = facilityReportService.createNewFacilityReport(facilityReportRequest);
        if (facilityReportID == -1) {
            throw new FacilityNotFoundException("The facility with the id of " + facilityReportRequest.getFacilityID() + " does not exist.");
        }

        return ResponseEntity.ok(FacilityReportResponse.builder()
                                                       .message("New facility report with the id of " + facilityReportID + " has been created.")
                                                       .build());
    }

    @PatchMapping(value = "/{facilityReportId}")
    public ResponseEntity<FacilityReportResponse> updateFacilityReport(@PathVariable Integer facilityReportId,
                                                                       @RequestParam String status) throws FacilityReportNotFoundException {
        if (facilityReportId < 1) { throw new RuntimeException("Invalid facility report ID."); }

        boolean isFacilityReportExist = facilityReportService.updateFacilityReport(facilityReportId, status);
        if (!isFacilityReportExist) {
            throw new FacilityReportNotFoundException("The facility report with the id of " + facilityReportId + " does not exist.");
        }

        return ResponseEntity.ok(FacilityReportResponse.builder()
                                                       .message("Facility Report with the id of " + facilityReportId + " has been updated.")
                                                       .build());
    }

    @GetMapping(value = "byFacilityReportId/{facilityReportId}")
    public ResponseEntity<FacilityReportResponse> getFacilityReportById(@PathVariable Integer facilityReportId) throws FacilityReportNotFoundException {
        if (facilityReportId < 1) { throw new RuntimeException("Invalid facility report ID."); }

        FacilityReport facilityReport = facilityReportService.getFacilityReportById(facilityReportId);
        if (facilityReport == null) {
            throw new FacilityReportNotFoundException("The facility report with the id of " + facilityReportId + " does not exist.");
        }

        return ResponseEntity.ok(FacilityReportResponse.builder()
                                                       .message("Returning facility report with the id of " + facilityReportId)
                                                       .facilityReport(facilityReport)
                                                       .build());
    }

    @GetMapping(value = "{facilityId}")
    public ResponseEntity<AllFacilityReportResponse> getAllFacilityReportsByFacilityId(@PathVariable Integer facilityId) throws FacilityNotFoundException {
        if (facilityId < 1) { throw new RuntimeException("Invalid facility ID."); }

        List<FacilityReport> facilityReportList = facilityReportService.getAllFacilityReportsByFacilityId(facilityId);
        if (facilityReportList.isEmpty()) {
            throw new FacilityNotFoundException("The facility with the id of " + facilityId + " does not exist.");
        }

        return ResponseEntity.ok(AllFacilityReportResponse.builder()
                                                          .message("Returning all facility reports with the facility id of " + facilityId)
                                                          .facilityReports(facilityReportList)
                                                          .build());
    }

    @GetMapping
    public ResponseEntity<AllFacilityReportResponse> getAllFacilityReports() throws FacilityReportNotFoundException {
        List<FacilityReport> facilityReportList = facilityReportService.getAllFacilityReports();
        if (facilityReportList.size() == 0) {
            throw new FacilityReportNotFoundException("No facility report exists in the database.");
        }

        return ResponseEntity.ok(AllFacilityReportResponse.builder()
                                                          .message("Returning all facility reports")
                                                          .facilityReports(facilityReportList)
                                                          .build());
    }
}
