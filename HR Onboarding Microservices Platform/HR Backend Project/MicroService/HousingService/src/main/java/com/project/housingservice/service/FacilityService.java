package com.project.housingservice.service;

import com.project.housingservice.dao.FacilityDAO;
import com.project.housingservice.domain.storage.hibernate.Facility;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class FacilityService {
    private FacilityDAO facilityDAO;

    @Autowired
    @Qualifier("facilityHibernateDAO")
    public void setFacilityDAO(FacilityDAO facilityDAO) {
        this.facilityDAO = facilityDAO;
    }

    @Transactional
    public List<Facility> getAllFacilitiesByHouseId(Integer houseId) {
        return facilityDAO.getAllFacilitiesByHouseId(houseId);
    }
}
