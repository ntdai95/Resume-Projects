package com.project.housingservice.dao.impl.hibernate;

import com.project.housingservice.dao.AbstractHibernateDAO;
import com.project.housingservice.dao.FacilityDAO;
import com.project.housingservice.domain.storage.hibernate.Facility;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository("facilityHibernateDAO")
public class FacilityHibernateDAO extends AbstractHibernateDAO<Facility> implements FacilityDAO {
    public FacilityHibernateDAO() {
        setClazz(Facility.class);
    }

    @Override
    public void createNewFacility(Facility facility) {
        add(facility);
    }

    @Override
    public List<Facility> getAllFacilitiesByHouseId(Integer houseId) {
        String query = "From Facility f join fetch f.house h where h.id = :houseId";
        List<Facility> facilityList = getCurrentSession().createQuery(query).setParameter("houseId", houseId).getResultList();
        return facilityList;
    }
}
