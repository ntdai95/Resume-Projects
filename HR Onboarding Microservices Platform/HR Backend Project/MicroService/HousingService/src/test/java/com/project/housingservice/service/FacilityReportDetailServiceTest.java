package com.project.housingservice.service;

import com.project.housingservice.dao.FacilityReportDetailDAO;
import com.project.housingservice.domain.request.FacilityReportDetail.FacilityReportDetailRequest;
import com.project.housingservice.domain.storage.hibernate.FacilityReportDetail;
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
public class FacilityReportDetailServiceTest {
    @InjectMocks
    FacilityReportDetailService facilityReportDetailService;

    @Mock
    FacilityReportDetailDAO facilityReportDetailDAO;

    FacilityReportDetail mockFacilityReportDetail;

    @BeforeEach
    public void setup() {
        mockFacilityReportDetail = FacilityReportDetail.builder()
                                                       .employeeID("hugegif")
                                                       .comment("Issue solved.")
                                                       .createDate("2022-08-16")
                                                       .lastModificationDate("2022-08-19")
                                                       .build();
    }

    @Test
    public void testGetAllFacilityReportDetailByFacilityReportId_success() {
        List<FacilityReportDetail> mockFacilityReportDetailList = new ArrayList<>();
        mockFacilityReportDetail.setId(1);
        mockFacilityReportDetailList.add(mockFacilityReportDetail);

        when(facilityReportDetailDAO.getAllFacilityReportDetailByFacilityReportId(1)).thenReturn(mockFacilityReportDetailList);
        List<FacilityReportDetail> facilityReportDetailList = facilityReportDetailService.getAllFacilityReportDetailByFacilityReportId(1);

        assertEquals(mockFacilityReportDetailList.get(0).getId(), facilityReportDetailList.get(0).getId());
        assertEquals(mockFacilityReportDetailList.get(0).getEmployeeID(), facilityReportDetailList.get(0).getEmployeeID());
        assertEquals(mockFacilityReportDetailList.get(0).getComment(), facilityReportDetailList.get(0).getComment());
        assertEquals(mockFacilityReportDetailList.get(0).getCreateDate(), facilityReportDetailList.get(0).getCreateDate());
        assertEquals(mockFacilityReportDetailList.get(0).getLastModificationDate(), facilityReportDetailList.get(0).getLastModificationDate());
    }

    @Test
    public void testCreateNewFacilityReportDetail_success() {
        FacilityReportDetailRequest mockFacilityReportDetailRequest = FacilityReportDetailRequest.builder()
                                                                                                 .FacilityReportID(1)
                                                                                                 .EmployeeID("hvirgg")
                                                                                                 .Comment("Issue still persist.")
                                                                                                 .build();

        when(facilityReportDetailDAO.createNewFacilityReportDetail(mockFacilityReportDetailRequest)).thenReturn(1);
        int facilityReportDetailId = facilityReportDetailService.createNewFacilityReportDetail(mockFacilityReportDetailRequest);
        assertEquals(1, facilityReportDetailId);
    }

    @Test
    public void testUpdateFacilityReportDetail_success() {
        when(facilityReportDetailDAO.updateFacilityReportDetail(1, "hugegif", "Closed")).thenReturn(true);
        boolean isSuccess = facilityReportDetailService.updateFacilityReportDetail(1, "hugegif", "Closed");
        assertTrue(isSuccess);
    }

    @Test
    public void testUpdateFacilityReportDetail_fail() {
        when(facilityReportDetailDAO.updateFacilityReportDetail(100, "hugegif", "Closed")).thenReturn(false);
        boolean isSuccess = facilityReportDetailService.updateFacilityReportDetail(100, "hugegif", "Closed");
        assertFalse(isSuccess);
    }
}
