package com.project.housingservice.service;

import com.project.housingservice.dao.FacilityReportDAO;
import com.project.housingservice.domain.request.FacilityReport.FacilityReportRequest;
import com.project.housingservice.domain.storage.hibernate.FacilityReport;
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
public class FacilityReportServiceTest {
    @InjectMocks
    FacilityReportService facilityReportService;

    @Mock
    FacilityReportDAO facilityReportDAO;

    FacilityReport mockFacilityReport;

    @BeforeEach
    public void setup() {
        mockFacilityReport = FacilityReport.builder()
                                           .employeeID("hvuowg")
                                           .title("Broken bed")
                                           .description("The legs of bed are broken.")
                                           .createDate("2022-08-16")
                                           .status("Open")
                                           .build();
    }

    @Test
    public void testCreateNewFacilityReport_success() {
        FacilityReportRequest mockFacilityReportRequest = FacilityReportRequest.builder()
                                                                               .FacilityID(1)
                                                                               .EmployeeID("ouver")
                                                                               .Title("Broken bed")
                                                                               .Description("The legs of bed are broken.")
                                                                               .build();

        when(facilityReportDAO.createNewFacilityReport(mockFacilityReportRequest)).thenReturn(1);
        int facilityReportId = facilityReportService.createNewFacilityReport(mockFacilityReportRequest);
        assertEquals(1, facilityReportId);
    }

    @Test
    public void testUpdateFacilityReport_success() {
        when(facilityReportDAO.updateFacilityReport(1, "Closed")).thenReturn(true);
        boolean isSuccess = facilityReportService.updateFacilityReport(1, "Closed");
        assertTrue(isSuccess);
    }

    @Test
    public void testUpdateFacilityReport_fail() {
        when(facilityReportDAO.updateFacilityReport(1, "Closed")).thenReturn(false);
        boolean isSuccess = facilityReportService.updateFacilityReport(1, "Closed");
        assertFalse(isSuccess);
    }

    @Test
    public void testGetAllFacilityReportsByFacilityId_success() {
        List<FacilityReport> mockFacilityReportList = new ArrayList<>();
        mockFacilityReport.setId(1);
        mockFacilityReportList.add(mockFacilityReport);

        when(facilityReportDAO.getAllFacilityReportsByFacilityId(1)).thenReturn(mockFacilityReportList);
        List<FacilityReport> facilityReportList = facilityReportService.getAllFacilityReportsByFacilityId(1);

        assertEquals(mockFacilityReportList.get(0).getId(), facilityReportList.get(0).getId());
        assertEquals(mockFacilityReportList.get(0).getEmployeeID(), facilityReportList.get(0).getEmployeeID());
        assertEquals(mockFacilityReportList.get(0).getTitle(), facilityReportList.get(0).getTitle());
        assertEquals(mockFacilityReportList.get(0).getDescription(), facilityReportList.get(0).getDescription());
        assertEquals(mockFacilityReportList.get(0).getCreateDate(), facilityReportList.get(0).getCreateDate());
        assertEquals(mockFacilityReportList.get(0).getStatus(), facilityReportList.get(0).getStatus());
    }

    @Test
    public void testGetAllFacilityReports_success() {
        List<FacilityReport> mockFacilityReportList = new ArrayList<>();
        mockFacilityReport.setId(1);
        mockFacilityReportList.add(mockFacilityReport);

        when(facilityReportDAO.getAllFacilityReports()).thenReturn(mockFacilityReportList);
        List<FacilityReport> facilityReportList = facilityReportService.getAllFacilityReports();

        assertEquals(mockFacilityReportList.get(0).getId(), facilityReportList.get(0).getId());
        assertEquals(mockFacilityReportList.get(0).getEmployeeID(), facilityReportList.get(0).getEmployeeID());
        assertEquals(mockFacilityReportList.get(0).getTitle(), facilityReportList.get(0).getTitle());
        assertEquals(mockFacilityReportList.get(0).getDescription(), facilityReportList.get(0).getDescription());
        assertEquals(mockFacilityReportList.get(0).getCreateDate(), facilityReportList.get(0).getCreateDate());
        assertEquals(mockFacilityReportList.get(0).getStatus(), facilityReportList.get(0).getStatus());
    }
}
