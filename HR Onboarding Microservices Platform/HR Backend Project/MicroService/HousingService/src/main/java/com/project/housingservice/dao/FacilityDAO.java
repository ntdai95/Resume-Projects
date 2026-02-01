package com.project.housingservice.dao;

import com.project.housingservice.domain.storage.hibernate.Facility;

import java.util.List;

public interface FacilityDAO {
    void createNewFacility(Facility facility);

    List<Facility> getAllFacilitiesByHouseId(Integer houseId);
}
