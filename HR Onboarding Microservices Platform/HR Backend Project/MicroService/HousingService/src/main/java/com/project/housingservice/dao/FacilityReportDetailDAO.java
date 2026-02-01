package com.project.housingservice.dao;

import com.project.housingservice.domain.request.FacilityReportDetail.FacilityReportDetailRequest;
import com.project.housingservice.domain.storage.hibernate.FacilityReportDetail;

import java.util.List;

public interface FacilityReportDetailDAO {
    List<FacilityReportDetail> getAllFacilityReportDetailByFacilityReportId(Integer facilityReportId);

    Integer createNewFacilityReportDetail(FacilityReportDetailRequest facilityReportDetailRequest);

    boolean updateFacilityReportDetail(Integer facilityReportDetailID, String employeeID, String newComment);
}
