package com.project.onboard.service.remote;

import com.project.onboard.domain.request.housing.FacilityReportDetailRequest;
import com.project.onboard.domain.request.housing.FacilityReportRequest;
import com.project.onboard.domain.response.housing.*;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;

@FeignClient("housing")
public interface RemoteHousingService {
    @GetMapping(value = "housing/house/{houseId}")
    HouseResponse getHouseDetailPageByHouseId(@PathVariable Integer houseId);

    @PostMapping(value = "housing/facilityReport")
    FacilityReportResponse createNewFacilityReport(@RequestBody FacilityReportRequest facilityReportRequest);

    @GetMapping(value = "housing/facilityReportDetail/{facilityReportId}")
    AllFacilityReportDetailResponse getAllFacilityReportDetailByFacilityReportId(@PathVariable Integer facilityReportId);

    @GetMapping(value = "housing/facilityReport")
    AllFacilityReportResponse getAllFacilityReports();

    @PostMapping(value = "housing/facilityReportDetail")
    FacilityReportDetailResponse createNewFacilityReportDetail(@RequestBody FacilityReportDetailRequest facilityReportDetailRequest);

    @PatchMapping(value = "housing/facilityReportDetail/{facilityReportDetailID}")
    FacilityReportDetailResponse updateFacilityReportDetail(@PathVariable Integer facilityReportDetailID,
                                                            @RequestParam String employeeID, @RequestParam String newComment);
}
