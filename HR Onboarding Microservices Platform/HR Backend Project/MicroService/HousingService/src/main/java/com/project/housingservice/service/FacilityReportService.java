package com.project.housingservice.service;

import com.project.housingservice.dao.FacilityReportDAO;
import com.project.housingservice.domain.request.FacilityReport.FacilityReportRequest;
import com.project.housingservice.domain.storage.hibernate.FacilityReport;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;

@Service
public class FacilityReportService {
    private FacilityReportDAO facilityReportDAO;

    @Autowired
    @Qualifier("facilityReportHibernateDAO")
    public void setFacilityReportDAO(FacilityReportDAO facilityReportDAO) {
        this.facilityReportDAO = facilityReportDAO;
    }

    @Transactional
    public Integer createNewFacilityReport(FacilityReportRequest facilityReportRequest) {
        return facilityReportDAO.createNewFacilityReport(facilityReportRequest);
    }

    @Transactional
    public boolean updateFacilityReport(Integer facilityReportId, String status) {
        return facilityReportDAO.updateFacilityReport(facilityReportId, status);
    }

    @Transactional
    public FacilityReport getFacilityReportById(Integer facilityReportId) {
        return facilityReportDAO.getFacilityReportById(facilityReportId);
    }

    @Transactional
    public List<FacilityReport> getAllFacilityReportsByFacilityId(Integer facilityId) {
        return facilityReportDAO.getAllFacilityReportsByFacilityId(facilityId);
    }

    @Transactional
    public List<FacilityReport> getAllFacilityReports() {
        return facilityReportDAO.getAllFacilityReports();
    }
}
