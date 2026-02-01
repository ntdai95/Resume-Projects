package com.project.housingservice.dao;

import com.project.housingservice.domain.request.FacilityReport.FacilityReportRequest;
import com.project.housingservice.domain.storage.hibernate.FacilityReport;

import java.util.List;

public interface FacilityReportDAO {
    Integer createNewFacilityReport(FacilityReportRequest facilityReportRequest);

    boolean updateFacilityReport(Integer facilityReportId, String status);

    FacilityReport getFacilityReportById(Integer facilityReportId);

    List<FacilityReport> getAllFacilityReportsByFacilityId(Integer facilityId);

    List<FacilityReport> getAllFacilityReports();
}
