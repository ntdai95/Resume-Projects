package com.project.housingservice.controller;

import com.google.gson.Gson;
import com.project.housingservice.domain.response.Error.ErrorResponse;
import com.project.housingservice.domain.response.Facility.AllFacilityResponse;
import com.project.housingservice.domain.storage.hibernate.Facility;
import com.project.housingservice.service.FacilityService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(FacilityController.class)
@ExtendWith(MockitoExtension.class)
class FacilityControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    FacilityService facilityService;

    @Test
    public void testGetAllFacilitiesByHouseId_success() throws Exception {
        List<Facility> mockFacilityList = new ArrayList<>();
        Facility mockFacility1 = Facility.builder()
                                         .id(1)
                                         .type("bed")
                                         .description("number of beds")
                                         .quantity(3)
                                         .build();
        Facility mockFacility2 = Facility.builder()
                                         .id(2)
                                         .type("table")
                                         .description("number of tables")
                                         .quantity(2)
                                         .build();
        mockFacilityList.add(mockFacility1);
        mockFacilityList.add(mockFacility2);

        AllFacilityResponse mockAllFacilityResponse = AllFacilityResponse.builder()
                                                                         .message("Returning all facilities with the house id of 1")
                                                                         .facilities(mockFacilityList)
                                                                         .build();

        when(facilityService.getAllFacilitiesByHouseId(1)).thenReturn(mockFacilityList);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facility/{houseId}", 1)
                                                                 .contentType(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        AllFacilityResponse allFacilityResponse = new Gson().fromJson(result.getResponse().getContentAsString(), AllFacilityResponse.class);
        assertTrue(allFacilityResponse.isSuccess());
        assertEquals(mockAllFacilityResponse.getMessage(), allFacilityResponse.getMessage());
        assertEquals(mockAllFacilityResponse.getFacilities().toString(), allFacilityResponse.getFacilities().toString());
    }

    @Test
    public void testGetAllFacilitiesByHouseId_InvalidIntegerHouseId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facility/{houseId}", -1)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "Invalid house ID.");
    }

    @Test
    public void testGetAllFacilitiesByHouseId_InvalidStringHouseId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facility/{houseId}", "a")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testGetAllFacilitiesByHouseId_HouseNotFound() throws Exception {
        List<Facility> mockFacilityList = new ArrayList<>();
        when(facilityService.getAllFacilitiesByHouseId(100)).thenReturn(mockFacilityList);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facility/{houseId}", 100)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The house with the id of 100 does not exist.");
    }
}