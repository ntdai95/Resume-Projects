package com.project.housingservice.service;

import com.project.housingservice.dao.FacilityDAO;
import com.project.housingservice.dao.HouseDAO;
import com.project.housingservice.domain.request.House.HouseRequest;
import com.project.housingservice.domain.storage.hibernate.House;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class HouseServiceTest {
    @InjectMocks
    HouseService houseService;

    @Mock
    HouseDAO houseDAO;

    @Mock
    FacilityDAO facilityDAO;

    House mockHouse;

    @BeforeEach
    public void setup() {
        mockHouse = House.builder()
                         .address("5674 Phoenix Rd")
                         .maxOccupant(3)
                         .build();
    }

    @Test
    public void testGetHouseById_success() {
        when(houseDAO.getHouseById(1)).thenReturn(mockHouse);
        House house = houseService.getHouseById(1);

        assertEquals(house.toString(), mockHouse.toString());
    }

    @Test
    public void testCreateNewHouse_success() {
        HouseRequest mockHouseRequest = HouseRequest.builder()
                                                    .LandlordID(1)
                                                    .Address("5674 Phoenix Rd")
                                                    .MaxOccupant(3)
                                                    .build();

        when(houseDAO.createNewHouse(any(), any())).thenReturn(1);
        int houseId = houseService.createNewHouse(mockHouseRequest);
        assertEquals(1, houseId);
    }

    @Test
    public void testDeleteHouseById_success() {
        when(houseDAO.deleteHouseById(1)).thenReturn(true);
        boolean isSuccess = houseService.deleteHouseById(1);
        assertTrue(isSuccess);
    }

    @Test
    public void testDeleteHouseById_fail() {
        when(houseDAO.deleteHouseById(1)).thenReturn(false);
        boolean isSuccess = houseService.deleteHouseById(1);
        assertFalse(isSuccess);
    }

    @Test
    public void testGetAllHouses_success() {
        List<House> mockHouseList = new ArrayList<>();
        mockHouse.setId(1);
        mockHouseList.add(mockHouse);

        when(houseDAO.getAllHouses()).thenReturn(mockHouseList);
        List<House> houseList = houseService.getAllHouses();

        assertEquals(mockHouseList.get(0).getId(), houseList.get(0).getId());
        assertEquals(mockHouseList.get(0).getAddress(), houseList.get(0).getAddress());
        assertEquals(mockHouseList.get(0).getMaxOccupant(), houseList.get(0).getMaxOccupant());
    }
}
