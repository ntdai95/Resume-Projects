package com.project.housingservice.service;

import com.project.housingservice.dao.FacilityReportDetailDAO;
import com.project.housingservice.domain.request.FacilityReportDetail.FacilityReportDetailRequest;
import com.project.housingservice.domain.storage.hibernate.FacilityReportDetail;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;

@Service
public class FacilityReportDetailService {
    private FacilityReportDetailDAO facilityReportDetailDAO;

    @Autowired
    @Qualifier("facilityReportDetailHibernateDAO")
    public void setFacilityReportDetailDAO(FacilityReportDetailDAO facilityReportDetailDAO) {
        this.facilityReportDetailDAO = facilityReportDetailDAO;
    }

    @Transactional
    public List<FacilityReportDetail> getAllFacilityReportDetailByFacilityReportId(Integer facilityReportId) {
        return facilityReportDetailDAO.getAllFacilityReportDetailByFacilityReportId(facilityReportId);
    }

    @Transactional
    public Integer createNewFacilityReportDetail(FacilityReportDetailRequest facilityReportDetailRequest) {
        return facilityReportDetailDAO.createNewFacilityReportDetail(facilityReportDetailRequest);
    }

    @Transactional
    public boolean updateFacilityReportDetail(Integer facilityReportDetailID, String employeeID, String newComment) {
        return facilityReportDetailDAO.updateFacilityReportDetail(facilityReportDetailID, employeeID, newComment);
    }
}
