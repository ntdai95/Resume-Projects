package com.project.hr.service.remote;

import com.project.hr.domain.request.housing.FacilityReportDetailRequest;
import com.project.hr.domain.request.housing.HouseRequest;
import com.project.hr.domain.response.housing.*;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;

@FeignClient("housing")
public interface RemoteHousingService {
    @PostMapping(value = "housing/house")
    HouseResponse createNewHouse(@RequestBody HouseRequest houseRequest);

    @DeleteMapping(value = "housing/house/{houseId}")
    HouseResponse deleteHouseById(@PathVariable Integer houseId);

    @GetMapping(value = "housing/house")
    AllHouseResponse getAllHouses();

    @GetMapping(value = "housing/house/{houseId}")
    HouseResponse getHouseById(@PathVariable Integer houseId);

    @GetMapping(value = "housing/facility/{houseId}")
    AllFacilityResponse getAllFacilitiesByHouseId(@PathVariable Integer houseId);

    @GetMapping(value = "housing/facilityReport/{facilityId}")
    AllFacilityReportResponse getAllFacilityReportsByFacilityId(@PathVariable Integer facilityId);

    @GetMapping(value = "housing/facilityReport/byFacilityReportId/{facilityReportId}")
    FacilityReportResponse getFacilityReportById(@PathVariable Integer facilityReportId);

    @GetMapping(value = "housing/facilityReportDetail/{facilityReportId}")
    AllFacilityReportDetailResponse getAllFacilityReportDetailByFacilityReportId(@PathVariable Integer facilityReportId);

    @PostMapping(value = "housing/facilityReportDetail")
    FacilityReportDetailResponse createNewFacilityReportDetail(@RequestBody FacilityReportDetailRequest facilityReportDetailRequest);

    @PatchMapping(value = "housing/facilityReportDetail/{facilityReportDetailID}")
    FacilityReportDetailResponse updateFacilityReportDetail(@PathVariable Integer facilityReportDetailID,
                                                            @RequestParam String employeeID, @RequestParam String newComment);
}
