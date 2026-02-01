package com.project.housingservice.service;

import com.project.housingservice.dao.FacilityDAO;
import com.project.housingservice.domain.storage.hibernate.Facility;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class FacilityServiceTest {
    @InjectMocks
    FacilityService facilityService;

    @Mock
    FacilityDAO facilityDAO;

    Facility mockFacility;

    @BeforeEach
    public void setup() {
        mockFacility = Facility.builder()
                               .type("bed")
                               .description("number of beds")
                               .quantity(3)
                               .build();
    }

    @Test
    public void testGetAllFacilitiesByHouseId_success() {
        List<Facility> mockFacilityList = new ArrayList<>();
        mockFacilityList.add(mockFacility);

        when(facilityDAO.getAllFacilitiesByHouseId(1)).thenReturn(mockFacilityList);
        List<Facility> facilityList = facilityService.getAllFacilitiesByHouseId(1);

        assertEquals(mockFacility, facilityList.get(0));
    }
}