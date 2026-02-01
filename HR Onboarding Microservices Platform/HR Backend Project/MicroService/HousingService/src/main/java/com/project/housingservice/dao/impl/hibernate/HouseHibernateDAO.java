package com.project.housingservice.dao.impl.hibernate;

import com.project.housingservice.dao.AbstractHibernateDAO;
import com.project.housingservice.dao.HouseDAO;
import com.project.housingservice.domain.request.House.HouseRequest;
import com.project.housingservice.domain.storage.hibernate.Facility;
import com.project.housingservice.domain.storage.hibernate.House;
import com.project.housingservice.domain.storage.hibernate.Landlord;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository("houseHibernateDAO")
public class HouseHibernateDAO extends AbstractHibernateDAO<House> implements HouseDAO {
    public HouseHibernateDAO() {
        setClazz(House.class);
    }

    @Override
    public House getHouseById(Integer houseId) {
        return findById(houseId);
    }

    @Override
    public Integer createNewHouse(HouseRequest houseRequest, List<Facility> facilities) {
        String query = "from Landlord where id = :id";
        List<Landlord> landlordList = getCurrentSession().createQuery(query).setParameter("id", houseRequest.getLandlordID()).getResultList();
        if (landlordList.isEmpty()) {
            return -1;
        }

        House house = House.builder()
                           .landlord(landlordList.get(0))
                           .address(houseRequest.getAddress())
                           .maxOccupant(houseRequest.getMaxOccupant())
                           .facilities(facilities)
                           .build();

        for (Facility facility : facilities) {
            facility.setHouse(house);
        }

        add(house);
        return house.getId();
    }

    @Override
    public boolean deleteHouseById(Integer houseId) {
        House house = findById(houseId);
        if (house == null) { return false; }

        getCurrentSession().delete(house);
        return true;
    }

    @Override
    public List<House> getAllHouses() {
        String query = "from House";
        List<House> houseList = getCurrentSession().createQuery(query).getResultList();
        return houseList;
    }
}