package com.project.housingservice.dao.impl.hibernate;

import com.project.housingservice.dao.AbstractHibernateDAO;
import com.project.housingservice.dao.FacilityReportDetailDAO;
import com.project.housingservice.domain.request.FacilityReportDetail.FacilityReportDetailRequest;
import com.project.housingservice.domain.storage.hibernate.FacilityReport;
import com.project.housingservice.domain.storage.hibernate.FacilityReportDetail;
import org.springframework.stereotype.Repository;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@Repository("facilityReportDetailHibernateDAO")
public class FacilityReportDetailHibernateDAO extends AbstractHibernateDAO<FacilityReportDetail> implements FacilityReportDetailDAO {
    public FacilityReportDetailHibernateDAO() {
        setClazz(FacilityReportDetail.class);
    }

    @Override
    public List<FacilityReportDetail> getAllFacilityReportDetailByFacilityReportId(Integer facilityReportId) {
        String query = "from FacilityReportDetail frd join fetch frd.facilityReport fr where fr.id = :facilityReportId";
        List<FacilityReportDetail> facilityReportDetailList = getCurrentSession().createQuery(query).setParameter("facilityReportId", facilityReportId).getResultList();
        return facilityReportDetailList;
    }

    @Override
    public Integer createNewFacilityReportDetail(FacilityReportDetailRequest facilityReportDetailRequest) {
        String query = "from FacilityReport where id = :id";
        List<FacilityReport> facilityReportList = getCurrentSession().createQuery(query).setParameter("id", facilityReportDetailRequest.getFacilityReportID()).getResultList();
        if (facilityReportList.isEmpty()) {
            return -1;
        }

        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date today = new Date();
        FacilityReportDetail facilityReportDetail = FacilityReportDetail.builder()
                                                                        .facilityReport(facilityReportList.get(0))
                                                                        .employeeID(facilityReportDetailRequest.getEmployeeID())
                                                                        .comment(facilityReportDetailRequest.getComment())
                                                                        .createDate(dateFormat.format(today))
                                                                        .lastModificationDate(dateFormat.format(today))
                                                                        .build();

        add(facilityReportDetail);
        return facilityReportDetail.getId();
    }

    @Override
    public boolean updateFacilityReportDetail(Integer facilityReportDetailID, String employeeID, String newComment) {
        FacilityReportDetail facilityReportDetail = findById(facilityReportDetailID);
        if (facilityReportDetail == null || !facilityReportDetail.getEmployeeID().equals(employeeID)) { return false; }

        facilityReportDetail.setComment(newComment);
        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date today = new Date();
        facilityReportDetail.setLastModificationDate(dateFormat.format(today));
        getCurrentSession().update(facilityReportDetail);
        return true;
    }
}
