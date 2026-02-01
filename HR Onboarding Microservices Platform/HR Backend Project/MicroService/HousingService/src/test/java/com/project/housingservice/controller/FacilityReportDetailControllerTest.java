package com.project.housingservice.controller;

import com.google.gson.Gson;
import com.project.housingservice.domain.request.FacilityReportDetail.FacilityReportDetailRequest;
import com.project.housingservice.domain.response.Error.ErrorResponse;
import com.project.housingservice.domain.response.FacilityReportDetail.AllFacilityReportDetailResponse;
import com.project.housingservice.domain.response.FacilityReportDetail.FacilityReportDetailResponse;
import com.project.housingservice.domain.storage.hibernate.FacilityReportDetail;
import com.project.housingservice.service.FacilityReportDetailService;
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

@WebMvcTest(FacilityReportDetailController.class)
@ExtendWith(MockitoExtension.class)
class FacilityReportDetailControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    FacilityReportDetailService facilityReportDetailService;

    @Test
    public void testGetAllFacilityReportDetailByFacilityReportId_success() throws Exception {
        List<FacilityReportDetail> mockFacilityReportDetailList = new ArrayList<>();
        FacilityReportDetail facilityReportDetail1 = FacilityReportDetail.builder()
                                                                         .id(1)
                                                                         .employeeID("hvuiwg")
                                                                         .comment("Issue solved.")
                                                                         .createDate("2022-08-16")
                                                                         .lastModificationDate("2022-08-17")
                                                                         .build();
        FacilityReportDetail facilityReportDetail2 = FacilityReportDetail.builder()
                                                                         .id(2)
                                                                         .employeeID("uvgw")
                                                                         .comment("Issue still persist.")
                                                                         .createDate("2022-08-18")
                                                                         .lastModificationDate("2022-08-19")
                                                                         .build();
        mockFacilityReportDetailList.add(facilityReportDetail1);
        mockFacilityReportDetailList.add(facilityReportDetail2);

        AllFacilityReportDetailResponse mockAllFacilityReportDetailResponse = AllFacilityReportDetailResponse.builder()
                                                                                                             .message("Returning all facility report details")
                                                                                                             .facilityReportDetails(mockFacilityReportDetailList)
                                                                                                             .build();

        when(facilityReportDetailService.getAllFacilityReportDetailByFacilityReportId(1)).thenReturn(mockFacilityReportDetailList);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReportDetail/{facilityReportId}", 1)
                                                                 .contentType(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        AllFacilityReportDetailResponse allFacilityReportDetailResponse = new Gson().fromJson(result.getResponse().getContentAsString(), AllFacilityReportDetailResponse.class);
        assertTrue(allFacilityReportDetailResponse.isSuccess());
        assertEquals(mockAllFacilityReportDetailResponse.getMessage(), allFacilityReportDetailResponse.getMessage());
        assertEquals(mockAllFacilityReportDetailResponse.getFacilityReportDetails().toString(), allFacilityReportDetailResponse.getFacilityReportDetails().toString());
    }

    @Test
    public void testGetAllFacilityReportDetailByFacilityReportId_InvalidIntegerFacilityReportId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReportDetail/{facilityReportId}", -1)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "Invalid facility report ID.");
    }

    @Test
    public void testGetAllFacilityReportDetailByFacilityReportId_InvalidStringFacilityReportId() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReportDetail/{facilityReportId}", "a")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testGetAllFacilityReportDetailByFacilityReportId_FacilityReportDetailNotFound() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/facilityReportDetail/{facilityReportId}", 100)
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "No facility report detail with the facility report id of 100 exists in the database.");
    }

    @Test
    public void testCreateNewFacilityReportDetail_success() throws Exception {
        FacilityReportDetailResponse mockFacilityReportDetailResponse = FacilityReportDetailResponse.builder()
                                                                                                    .message("New facility report detail with the id of 1 has been created.")
                                                                                                    .build();

        FacilityReportDetailRequest createMockFacilityReportDetailRequest = FacilityReportDetailRequest.builder()
                                                                                                       .FacilityReportID(1)
                                                                                                       .EmployeeID("hvuow")
                                                                                                       .Comment("Issue solved.")
                                                                                                       .build();

        when(facilityReportDetailService.createNewFacilityReportDetail(any())).thenReturn(1);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/facilityReportDetail")
                                                                 .contentType(MediaType.APPLICATION_JSON)
                                                                 .content(new Gson().toJson(createMockFacilityReportDetailRequest))
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        FacilityReportDetailResponse facilityReportDetailResponse = new Gson().fromJson(result.getResponse().getContentAsString(), FacilityReportDetailResponse.class);
        assertTrue(facilityReportDetailResponse.isSuccess());
        assertEquals(mockFacilityReportDetailResponse.getMessage(), facilityReportDetailResponse.getMessage());
    }

    @Test
    public void testCreateNewFacilityReportDetail_NoRequestBody() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/facilityReportDetail")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testCreateNewFacilityReportDetail_FacilityReportNotFound() throws Exception {
        FacilityReportDetailRequest createMockFacilityReportDetailRequest = FacilityReportDetailRequest.builder()
                                                                                                       .FacilityReportID(-1)
                                                                                                       .EmployeeID("hvuwr")
                                                                                                       .Comment("Issue solved.")
                                                                                                       .build();

        when(facilityReportDetailService.createNewFacilityReportDetail(any())).thenReturn(-1);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/facilityReportDetail")
                                                                 .contentType(MediaType.APPLICATION_JSON)
                                                                 .content(new Gson().toJson(createMockFacilityReportDetailRequest))
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The facility report with the id of -1 does not exist.");
    }

    @Test
    public void testUpdateFacilityReportDetail_success() throws Exception {
        FacilityReportDetailResponse mockFacilityReportDetailResponse = FacilityReportDetailResponse.builder()
                                                                                                    .message("Facility Report Detail with the id of 1 has been updated.")
                                                                                                    .build();

        when(facilityReportDetailService.updateFacilityReportDetail(1, "uigw", "Issue solved.")).thenReturn(true);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReportDetail/{facilityReportDetailID}", 1)
                                                                 .param("employeeID", "uigw")
                                                                 .param("newComment", "Issue solved.")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        FacilityReportDetailResponse facilityReportDetailResponse = new Gson().fromJson(result.getResponse().getContentAsString(), FacilityReportDetailResponse.class);
        assertTrue(facilityReportDetailResponse.isSuccess());
        assertEquals(mockFacilityReportDetailResponse.getMessage(), facilityReportDetailResponse.getMessage());
    }

    @Test
    public void testUpdateFacilityReportDetail_InvalidIntegerFacilityReportDetailID() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReportDetail/{facilityReportDetailID}", -1)
                                                                 .param("employeeID", "1")
                                                                 .param("newComment", "Issue solved.")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "Invalid facility report detail ID.");
    }

    @Test
    public void testUpdateFacilityReportDetail_InvalidStringFacilityReportDetailID() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReportDetail/{facilityReportDetailID}", "a")
                        .param("employeeID", "1")
                        .param("newComment", "Issue solved.")
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testUpdateFacilityReportDetail_InvalidStringEmployeeID() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReportDetail/{facilityReportDetailID}", 1)
                                                                 .param("employeeID", "a")
                                                                 .param("newComment", "Issue solved.")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertNotNull(errorResponse.getMessage());
    }

    @Test
    public void testUpdateFacilityReportDetail_FacilityReportDetailNotFound() throws Exception {
        when(facilityReportDetailService.updateFacilityReportDetail(100, "yv79wg", "Issue solved.")).thenReturn(false);
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.patch("/facilityReportDetail/{facilityReportDetailID}", 100)
                                                                 .param("employeeID", "1")
                                                                 .param("newComment", "Issue solved.")
                                                                 .accept(MediaType.APPLICATION_JSON))
                                  .andExpect(status().isOk())
                                  .andReturn();

        ErrorResponse errorResponse = new Gson().fromJson(result.getResponse().getContentAsString(), ErrorResponse.class);
        assertFalse(errorResponse.isSuccess());
        assertEquals(errorResponse.getMessage(), "The facility report detail with the id of 100 does not exist or you did not created this facility report detail.");
    }
}