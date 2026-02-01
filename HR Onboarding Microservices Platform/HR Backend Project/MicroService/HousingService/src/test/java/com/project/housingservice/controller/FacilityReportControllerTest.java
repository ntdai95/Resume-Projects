package com.project.housingservice.controller;


import com.google.gson.Gson;
import com.project.housingservice.domain.request.FacilityReport.FacilityReportRequest;
import com.project.housingservice.domain.response.Error.ErrorResponse;
import com.project.housingservice.domain.response.FacilityReport.AllFacilityReportResponse;
import com.project.housingservice.domain.response.FacilityReport.FacilityReportResponse;
import com.project.housingservice.domain.storage.hibernate.FacilityReport;
import com.project.housingservice.service.FacilityReportService;
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

@WebMvcTest(FacilityReportController.class)
@ExtendWith(MockitoExtension.class)
class FacilityReportControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    FacilityReportService facilityReportService;

    @Test
    public void testCreateNewFacilityReport_success() throws Exception {
        FacilityReportResponse mockFacilityReportResponse = FacilityReportResponse.builder()
                                                                                  .message("New facility report with the id of 1 has been created.")
                                                                                  .build();

        FacilityReportRequest createMockFacilityReportRequest = FacilityReportRequest.builder()
                                                                                     .FacilityID(1)
                                                                                     .EmployeeID("huguiwrgv")
                                                                                     .Title("Broken Chair")
                                                                                     .Description("The legs of the chair are broken.")
                                                                                     .build();

        when(facilityReportService.createNewFacilityReport(any())).thenReturn(1);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/facilityReport")
                                                                 .contentType(MediaType.APPLICATION_JSON)
                                                                 .content(new Gson().toJson(createMockFacilityReportRequest))
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        FacilityReportResponse facilityReportResponse = new Gson().fromJson(result.getResponse().getContentAsString(), FacilityReportResponse.class);
        assertTrue(facilityReportResponse.isSuccess());
        assertEquals(mockFacilityReportResponse.getMessage(), facilityReportResponse.getMessage());
    }

    @Test
    public void testCreateNewFacilityReport_NoRequestBody() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/facilityReport")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testCreateNewFacilityReport_FacilityNotFound() throws Exception {
        FacilityReportRequest createMockFacilityReportRequest = FacilityReportRequest.builder()
                                                                                     .FacilityID(-1)
                                                                                     .EmployeeID("hurgruvg")
                                                                                     .Title("Broken Chair")
                                                                                     .Description("The legs of the chair are broken.")
                                                                                     .build();

        when(facilityReportService.createNewFacilityReport(any())).thenReturn(-1);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/facilityReport")
                                                                 .contentType(MediaType.APPLICATION_JSON)
                                                                 .content(new Gson().toJson(createMockFacilityReportRequest))
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The facility with the id of -1 does not exist.");
    }

    @Test
    public void testUpdateFacilityReport_success() throws Exception {
        FacilityReportResponse mockFacilityReportResponse = FacilityReportResponse.builder()
                                                                                  .message("Facility Report with the id of 1 has been updated.")
                                                                                  .build();

        when(facilityReportService.updateFacilityReport(1, "Closed")).thenReturn(true);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReport/{facilityReportId}", 1)
                                                                 .param("status", "Closed")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        FacilityReportResponse facilityReportResponse = new Gson().fromJson(result.getResponse().getContentAsString(), FacilityReportResponse.class);
        assertTrue(facilityReportResponse.isSuccess());
        assertEquals(mockFacilityReportResponse.getMessage(), facilityReportResponse.getMessage());
    }

    @Test
    public void testUpdateFacilityReport_InvalidIntegerFacilityReportId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReport/{facilityReportId}", -1)
                                                                 .param("status", "Closed")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "Invalid facility report ID.");
    }

    @Test
    public void testUpdateFacilityReport_InvalidStringFacilityReportId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReport/{facilityReportId}", "a")
                                                                 .param("status", "Closed")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testUpdateFacilityReport_FacilityReportNotFound() throws Exception {
        when(facilityReportService.updateFacilityReport(100, "Closed")).thenReturn(false);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReport/{facilityReportId}", 100)
                                                                 .param("status", "Closed")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The facility report with the id of 100 does not exist.");
    }

    @Test
    public void testGetAllFacilityReportsByFacilityId_success() throws Exception {
        List<FacilityReport> mockFacilityReportList = new ArrayList<>();
        FacilityReport mockFacilityReport1 = FacilityReport.builder()
                                                          .id(1)
                                                          .employeeID("vbugrvi")
                                                          .title("Broken Chair")
                                                          .description("The legs of chair are broken.")
                                                          .createDate("2022-08-16")
                                                          .status("Open")
                                                          .build();
        FacilityReport mockFacilityReport2 = FacilityReport.builder()
                                                           .id(2)
                                                           .employeeID("vygrwuygv")
                                                           .title("Broken Table")
                                                           .description("The legs of table are broken.")
                                                           .createDate("2022-08-19")
                                                           .status("Closed")
                                                           .build();
        mockFacilityReportList.add(mockFacilityReport1);
        mockFacilityReportList.add(mockFacilityReport2);

        AllFacilityReportResponse mockAllFacilityReportResponse = AllFacilityReportResponse.builder()
                                                                                           .message("Returning all facility reports with the facility id of 1")
                                                                                           .facilityReports(mockFacilityReportList)
                                                                                           .build();

        when(facilityReportService.getAllFacilityReportsByFacilityId(1)).thenReturn(mockFacilityReportList);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReport/{facilityId}", 1)
                                                                 .contentType(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        AllFacilityReportResponse allFacilityReportResponse = new Gson().fromJson(result.getResponse().getContentAsString(), AllFacilityReportResponse.class);
        assertTrue(allFacilityReportResponse.isSuccess());
        assertEquals(mockAllFacilityReportResponse.getMessage(), allFacilityReportResponse.getMessage());
        assertEquals(mockAllFacilityReportResponse.getFacilityReports().toString(), allFacilityReportResponse.getFacilityReports().toString());
    }

    @Test
    public void testGetAllFacilityReportsByFacilityId_InvalidIntegerFacilityReportId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReport/{facilityId}", -1)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "Invalid facility ID.");
    }

    @Test
    public void testGetAllFacilityReportsByFacilityId_InvalidStringFacilityReportId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReport/{facilityId}", "a")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testGetAllFacilityReportsByFacilityId_FacilityNotFound() throws Exception {
        List<FacilityReport> mockFacilityReportList = new ArrayList<>();
        when(facilityReportService.getAllFacilityReportsByFacilityId(100)).thenReturn(mockFacilityReportList);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReport/{facilityId}", 100)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The facility with the id of 100 does not exist.");
    }

    @Test
    public void testGetAllFacilityReports_success() throws Exception {
        List<FacilityReport> mockFacilityReportList = new ArrayList<>();
        FacilityReport facilityReport1 = FacilityReport.builder()
                                                       .id(1)
                                                       .employeeID("uovigw")
                                                       .title("Broken Chair")
                                                       .description("The legs of chair are broken.")
                                                       .createDate("2022-08-16")
                                                       .status("Open")
                                                       .build();
        FacilityReport facilityReport2 = FacilityReport.builder()
                                                       .id(2)
                                                       .employeeID("iuveyw")
                                                       .title("Broken Desk")
                                                       .description("The legs of desk are broken.")
                                                       .createDate("2022-08-17")
                                                       .status("Closed")
                                                       .build();
        mockFacilityReportList.add(facilityReport1);
        mockFacilityReportList.add(facilityReport2);

        AllFacilityReportResponse mockAllFacilityReportResponse = AllFacilityReportResponse.builder()
                                                                                           .message("Returning all facility reports")
                                                                                           .facilityReports(mockFacilityReportList)
                                                                                           .build();

        when(facilityReportService.getAllFacilityReports()).thenReturn(mockFacilityReportList);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReport")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        AllFacilityReportResponse allFacilityReportResponse = new Gson().fromJson(result.getResponse().getContentAsString(), AllFacilityReportResponse.class);
        assertTrue(allFacilityReportResponse.isSuccess());
        assertEquals(mockAllFacilityReportResponse.getMessage(), allFacilityReportResponse.getMessage());
        assertEquals(mockAllFacilityReportResponse.getFacilityReports().toString(), allFacilityReportResponse.getFacilityReports().toString());
    }

    @Test
    public void testGetAllFacilityReports_FacilityReportNotFound() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReport")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "No facility report exists in the database.");
    }
}