package com.project.housingservice.service;

import com.project.housingservice.dao.FacilityDAO;
import com.project.housingservice.dao.HouseDAO;
import com.project.housingservice.domain.request.House.HouseRequest;
import com.project.housingservice.domain.storage.hibernate.Facility;
import com.project.housingservice.domain.storage.hibernate.House;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

@Service
public class HouseService {
    private HouseDAO houseDAO;

    private FacilityDAO facilityDAO;

    @Autowired
    @Qualifier("houseHibernateDAO")
    public void setHouseDAO(HouseDAO houseDAO) {
        this.houseDAO = houseDAO;
    }

    @Autowired
    @Qualifier("facilityHibernateDAO")
    public void setFacilityDAO(FacilityDAO facilityDAO) {
        this.facilityDAO = facilityDAO;
    }

    @Transactional
    public House getHouseById(Integer houseId) {
        return houseDAO.getHouseById(houseId);
    }

    @Transactional
    public Integer createNewHouse(HouseRequest houseRequest) {
        List<Facility> facilities = new ArrayList<>();
        Facility bed = Facility.builder()
                               .type("bed")
                               .description("number of beds")
                               .quantity(4)
                               .build();
        facilityDAO.createNewFacility(bed);
        facilities.add(bed);

        Facility mattress = Facility.builder()
                                    .type("mattress")
                                    .description("number of mattresses")
                                    .quantity(4)
                                    .build();
        facilityDAO.createNewFacility(mattress);
        facilities.add(mattress);

        Facility table = Facility.builder()
                                 .type("table")
                                 .description("number of tables")
                                 .quantity(1)
                                 .build();
        facilityDAO.createNewFacility(table);
        facilities.add(table);

        Facility chair = Facility.builder()
                                 .type("chair")
                                 .description("number of chairs")
                                 .quantity(8)
                                 .build();
        facilityDAO.createNewFacility(chair);
        facilities.add(chair);

        return houseDAO.createNewHouse(houseRequest, facilities);
    }

    @Transactional
    public boolean deleteHouseById(Integer houseId) {
        return houseDAO.deleteHouseById(houseId);
    }

    @Transactional
    public List<House> getAllHouses() {
        return houseDAO.getAllHouses();
    }
}
