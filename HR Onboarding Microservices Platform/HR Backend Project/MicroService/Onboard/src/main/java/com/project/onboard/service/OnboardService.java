package com.project.onboard.service;

import com.project.onboard.domain.request.application.ApplicationWorkFlowRequest;
import com.project.onboard.domain.request.employee.EmployeeRequest;
import com.project.onboard.domain.request.housing.FacilityReportDetailRequest;
import com.project.onboard.domain.request.housing.FacilityReportRequest;
import com.project.onboard.domain.request.user.RegisterUserRequest;
import com.project.onboard.domain.response.application.ApplicationWorkFlowResponse;
import com.project.onboard.domain.response.employee.Employee;
import com.project.onboard.domain.response.employee.EmployeeVisaInfo;
import com.project.onboard.domain.response.housing.*;
import com.project.onboard.domain.response.storage.FileResponse;
import com.project.onboard.domain.response.user.DigitalDocumentResponse;
import com.project.onboard.domain.response.user.RegisterUserResponse;
import com.project.onboard.exception.EmployeeNotFoundException;
import com.project.onboard.service.remote.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@Service
public class OnboardService {

    private final RemoteUserService userService;
    private final RemoteApplicationService applicationWorkFlowService;
    private final RemoteHousingService remoteHousingService;
    private final RemoteEmployeeService employeeService;
    private final RemoteStorageService storageService;

    @Autowired
    public OnboardService(RemoteUserService userService, RemoteApplicationService applicationWorkFlowService,
                          RemoteHousingService remoteHousingService, RemoteEmployeeService employeeService,
                          RemoteStorageService storageService) {
        this.userService = userService;
        this.applicationWorkFlowService = applicationWorkFlowService;
        this.remoteHousingService = remoteHousingService;
        this.employeeService = employeeService;
        this.storageService = storageService;
    }
    // ####################################    User Service    ########################################

    public RegisterUserResponse registerUser(RegisterUserRequest request, String token) {
        return userService.registerUser(request, token);
    }

    // ####################################    Application Service    ########################################

    public ApplicationWorkFlowResponse getApplicationWorkFlowById(String id) {
        return applicationWorkFlowService.getApplicationWorkFlowById(id);
    }

    public List<DigitalDocumentResponse> getAllDigitalDocument() {
        return applicationWorkFlowService.getAllDigitalDocument();
    }

    public ApplicationWorkFlowResponse createApplicationWorkFlow(ApplicationWorkFlowRequest request) {
        return applicationWorkFlowService.createApplicationWorkFlow(request);
    }

    // ####################################    House Service    ########################################

    public HouseResponse getHouseDetailPageByHouseId(Integer houseId) {
        return remoteHousingService.getHouseDetailPageByHouseId(houseId);
    }

    public FacilityReportResponse createNewFacilityReport(FacilityReportRequest facilityReportRequest) {
        return remoteHousingService.createNewFacilityReport(facilityReportRequest);
    }

    public AllFacilityReportDetailResponse getAllFacilityReportDetailByFacilityReportId(Integer facilityReportId) {
        return remoteHousingService.getAllFacilityReportDetailByFacilityReportId(facilityReportId);
    }

    public AllFacilityReportResponse getAllFacilityReports() {
        return remoteHousingService.getAllFacilityReports();
    }

    public FacilityReportDetailResponse createNewFacilityReportDetail(FacilityReportDetailRequest facilityReportDetailRequest) {
        return remoteHousingService.createNewFacilityReportDetail(facilityReportDetailRequest);
    }

    public FacilityReportDetailResponse updateFacilityReportDetail(Integer facilityReportDetailID, String employeeID,
                                                                   String newComment) {
        return remoteHousingService.updateFacilityReportDetail(facilityReportDetailID, employeeID, newComment);
    }

    // ####################################    Employee Service    ########################################

    public Employee create(EmployeeRequest request) {
        return employeeService.create(request);
    }

    public Employee updateEmployee(Employee e) {
        return employeeService.updateEmployee(e);
    }

    public Employee updateEmployeeById(String id, EmployeeRequest request) throws EmployeeNotFoundException {
        return employeeService.updateEmployeeById(id, request);
    }

    public Employee getEmployeeById(String id) throws EmployeeNotFoundException {
        return employeeService.getEmployeeById(id);
    }

    public List<Employee> findAllEmployee() {
        return employeeService.findAllEmployee();
    }

    public List<Employee> findAllEmployeeOrderByFirstNameAsc() {
        return employeeService.findAllEmployeeOrderByFirstNameAsc();
    }

    public List<Employee> findAllEmployeeOrderByEmailAsc() {
        return employeeService.findAllEmployeeOrderByEmailAsc();
    }

    public List<EmployeeVisaInfo> getAllEmployeeVisaInfo() {
        return employeeService.getAllEmployeeVisaInfo();
    }

    public List<Employee> getAllEmployeeInSameHouse(String houseId) {
        return employeeService.getAllEmployeeInSameHouse(houseId);
    }

    public String getEmployeeHouseIdByEmployeeId(String id) throws EmployeeNotFoundException {
        return employeeService.getEmployeeHouseIdByEmployeeId(id);
    }

    // ####################################    Storage Service    ########################################

    public FileResponse uploadFile(MultipartFile file){
        return storageService.uploadFile(file);
    }

    public ResponseEntity<ByteArrayResource> downloadFile(String fileName) {
        return storageService.downloadFile(fileName);
    }

    public ResponseEntity<String> deleteFile(String fileName) {
        return storageService.deleteFile(fileName);
    }
}
