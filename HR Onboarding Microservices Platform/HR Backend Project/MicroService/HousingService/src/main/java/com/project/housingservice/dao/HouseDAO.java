package com.project.housingservice.dao;

import com.project.housingservice.domain.request.House.HouseRequest;
import com.project.housingservice.domain.storage.hibernate.Facility;
import com.project.housingservice.domain.storage.hibernate.House;

import java.util.List;

public interface HouseDAO {
    House getHouseById(Integer houseId);

    Integer createNewHouse(HouseRequest houseRequest, List<Facility> facilities);

    boolean deleteHouseById(Integer houseId);

    List<House> getAllHouses();
}
