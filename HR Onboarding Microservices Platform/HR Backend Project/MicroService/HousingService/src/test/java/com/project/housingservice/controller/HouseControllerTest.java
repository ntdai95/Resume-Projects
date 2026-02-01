package com.project.housingservice.controller;

import com.google.gson.Gson;
import com.project.housingservice.domain.request.House.HouseRequest;
import com.project.housingservice.domain.response.Error.ErrorResponse;
import com.project.housingservice.domain.response.House.AllHouseResponse;
import com.project.housingservice.domain.response.House.HouseResponse;
import com.project.housingservice.domain.storage.hibernate.House;
import com.project.housingservice.service.HouseService;
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
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(HouseController.class)
@ExtendWith(MockitoExtension.class)
class HouseControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    HouseService houseService;

    @Test
    public void testGetHouseById_success() throws Exception {
        House mockHouse = House.builder()
                               .id(1)
                               .address("7533 Wing Ave")
                               .maxOccupant(3)
                               .build();

        HouseResponse mockHouseResponse = HouseResponse.builder()
                                                       .message("Returning house with the id of 1")
                                                       .house(mockHouse)
                                                       .build();

        when(houseService.getHouseById(1)).thenReturn(mockHouse);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/house/{houseId}", "1")
                                                                 .contentType(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        HouseResponse houseResponse = new Gson().fromJson(result.getResponse().getContentAsString(), HouseResponse.class);
        assertTrue(houseResponse.isSuccess());
        assertEquals(mockHouseResponse.getMessage(), houseResponse.getMessage());
        assertEquals(mockHouseResponse.getHouse().getId(), houseResponse.getHouse().getId());
        assertEquals(mockHouseResponse.getHouse().getAddress(), houseResponse.getHouse().getAddress());
        assertEquals(mockHouseResponse.getHouse().getMaxOccupant(), houseResponse.getHouse().getMaxOccupant());
    }

    @Test
    public void testGetHouseById_InvalidIntegerHouseId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/house/{houseId}", "-1")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "Invalid house ID.");
    }

    @Test
    public void testGetHouseById_InvalidStringHouseId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/house/{houseId}", "a")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testGetHouseById_HouseNotFound() throws Exception {
        when(houseService.getHouseById(1)).thenReturn(null);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/house/{houseId}", 1)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The house with the id of 1 does not exist.");
    }

    @Test
    public void testCreateNewHouse_success() throws Exception {
        HouseResponse mockHouseResponse = HouseResponse.builder()
                                                       .message("New house with the id of 1 has been created.")
                                                       .build();

        HouseRequest createMockHouseRequest = HouseRequest.builder()
                                                          .LandlordID(1)
                                                          .Address("7673 night Rd")
                                                          .MaxOccupant(2)
                                                          .build();

        when(houseService.createNewHouse(any())).thenReturn(1);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/house")
                                                                 .contentType(MediaType.APPLICATION_JSON)
                                                                 .content(new Gson().toJson(createMockHouseRequest))
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        HouseResponse houseResponse = new Gson().fromJson(result.getResponse().getContentAsString(), HouseResponse.class);
        assertTrue(houseResponse.isSuccess());
        assertEquals(mockHouseResponse.getMessage(), houseResponse.getMessage());
    }

    @Test
    public void testCreateNewHouse_NoRequestBody() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/house")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testCreateNewHouse_LandlordNotFound() throws Exception {
        HouseRequest createMockHouseRequest = HouseRequest.builder()
                                                          .LandlordID(-1)
                                                          .Address("7673 night Rd")
                                                          .MaxOccupant(2)
                                                          .build();

        when(houseService.createNewHouse(any())).thenReturn(-1);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/house")
                                                                 .contentType(MediaType.APPLICATION_JSON)
                                                                 .content(new Gson().toJson(createMockHouseRequest))
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The landlord with the id of -1 does not exist.");
    }

    @Test
    public void testDeleteHouseById_success() throws Exception {
        when(houseService.deleteHouseById(1)).thenReturn(true);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.delete("/house/{houseId}", 1)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        HouseResponse houseResponse = new Gson().fromJson(result.getResponse().getContentAsString(), HouseResponse.class);
        assertTrue(houseResponse.isSuccess());
        assertEquals(houseResponse.getMessage(), "House with the id of 1 has been deleted.");
    }

    @Test
    public void testDeleteHouseById_InvalidIntegerHouseId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.delete("/house/{houseId}", -1)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "Invalid house ID.");
    }

    @Test
    public void testDeleteHouseById_InvalidStringHouseId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.delete("/house/{houseId}", "a")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testDeleteHouseById_HouseNotFound() throws Exception {
        when(houseService.deleteHouseById(100)).thenReturn(false);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.delete("/house/{houseId}", 100)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The house with the id of 100 does not exist.");
    }

    @Test
    public void testGetAllHouses_success() throws Exception {
        List<House> mockHouseList = new ArrayList<>();
        House house1 = House.builder()
                            .id(1)
                            .address("7634 Kilo drive")
                            .maxOccupant(3)
                            .build();
        House house2 = House.builder()
                            .id(2)
                            .address("9234 View drive")
                            .maxOccupant(2)
                            .build();
        mockHouseList.add(house1);
        mockHouseList.add(house2);

        AllHouseResponse mockAllHouseResponse = AllHouseResponse.builder()
                                                                .message("Returning all houses")
                                                                .houses(mockHouseList)
                                                                .build();

        when(houseService.getAllHouses()).thenReturn(mockHouseList);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/house")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        AllHouseResponse allHouseResponse = new Gson().fromJson(result.getResponse().getContentAsString(), AllHouseResponse.class);
        assertTrue(allHouseResponse.isSuccess());
        assertEquals(mockAllHouseResponse.getMessage(), allHouseResponse.getMessage());
        assertEquals(mockAllHouseResponse.getHouses().toString(), allHouseResponse.getHouses().toString());
    }

    @Test
    public void testGetAllHouses_HouseNotFound() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/house")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                                                 .andExpect(status().isOk())
                                                                 .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "No house detail exists in the database.");
    }
}