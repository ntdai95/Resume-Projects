package com.project.housingservice.dao.impl.hibernate;

import com.project.housingservice.dao.AbstractHibernateDAO;
import com.project.housingservice.dao.FacilityReportDAO;
import com.project.housingservice.domain.request.FacilityReport.FacilityReportRequest;
import com.project.housingservice.domain.storage.hibernate.Facility;
import com.project.housingservice.domain.storage.hibernate.FacilityReport;
import org.springframework.stereotype.Repository;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@Repository("facilityReportHibernateDAO")
public class FacilityReportHibernateDAO extends AbstractHibernateDAO<FacilityReport> implements FacilityReportDAO {
    public FacilityReportHibernateDAO() {
        setClazz(FacilityReport.class);
    }

    @Override
    public Integer createNewFacilityReport(FacilityReportRequest facilityReportRequest) {
        String query = "from Facility where id = :id";
        List<Facility> facilityList = getCurrentSession().createQuery(query).setParameter("id", facilityReportRequest.getFacilityID()).getResultList();
        if (facilityList.isEmpty()) {
            return -1;
        }

        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date today = new Date();
        FacilityReport facilityReport = FacilityReport.builder()
                                                      .facility(facilityList.get(0))
                                                      .employeeID(facilityReportRequest.getEmployeeID())
                                                      .title(facilityReportRequest.getTitle())
                                                      .description(facilityReportRequest.getDescription())
                                                      .createDate(dateFormat.format(today))
                                                      .status("Open")
                                                      .build();

        add(facilityReport);
        return facilityReport.getId();
    }

    @Override
    public boolean updateFacilityReport(Integer facilityReportId, String status) {
        FacilityReport facilityReport = findById(facilityReportId);
        if (facilityReport == null) { return false; }

        facilityReport.setStatus(status);
        getCurrentSession().update(facilityReport);
        return true;
    }

    @Override
    public FacilityReport getFacilityReportById(Integer facilityReportId) {
        return findById(facilityReportId);
    }

    @Override
    public List<FacilityReport> getAllFacilityReportsByFacilityId(Integer facilityId) {
        String query = "from FacilityReport fr join fetch fr.facility f where f.id = :facilityId ORDER BY fr.createDate DESC";
        List<FacilityReport> facilityReportList = getCurrentSession().createQuery(query).setParameter("facilityId", facilityId).getResultList();
        return facilityReportList;
    }

    @Override
    public List<FacilityReport> getAllFacilityReports() {
        String query = "from FacilityReport fr ORDER BY fr.createDate DESC";
        List<FacilityReport> facilityReportList = getCurrentSession().createQuery(query).getResultList();
        return facilityReportList;
    }
}
