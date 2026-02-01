package com.project.hr.service;

import com.project.hr.domain.request.application.ApplicationWorkFlowRequest;
import com.project.hr.domain.request.housing.FacilityReportDetailRequest;
import com.project.hr.domain.request.housing.HouseRequest;
import com.project.hr.domain.request.registration.RegistrationToken;
import com.project.hr.domain.request.application.DigitalDocumentRequest;
import com.project.hr.domain.request.employee.EmployeeRequest;
import com.project.hr.domain.response.application.ApplicationWorkFlow;
import com.project.hr.domain.response.application.ApplicationWorkFlowResponse;
import com.project.hr.domain.response.application.DigitalDocumentResponse;
import com.project.hr.domain.response.employee.Employee;
import com.project.hr.domain.response.employee.EmployeeVisaInfo;
import com.project.hr.domain.response.housing.*;
import com.project.hr.domain.response.registration.RegistrationTokenResponse;
import com.project.hr.domain.response.storage.FileResponse;
import com.project.hr.exception.DigitalDocumentNotFoundException;
import com.project.hr.exception.EmployeeNotFoundException;
import com.project.hr.service.remote.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@Service
public class HRService {

    private final RemoteUserService userService;
    private final RemoteApplicationService applicationService;
    private final RemoteEmployeeService employeeService;
    private final RemoteStorageService storageService;

    private final RemoteHousingService housingService;

    @Autowired
    public HRService(RemoteUserService userService, RemoteApplicationService applicationService,
                     RemoteEmployeeService employeeService, RemoteStorageService storageService,
                     RemoteHousingService housingService) {
        this.userService = userService;
        this.applicationService = applicationService;
        this.employeeService = employeeService;
        this.storageService = storageService;
        this.housingService = housingService;
    }

    // ####################################    User Service    ########################################
    public RegistrationTokenResponse createToken(RegistrationToken request) {
        return userService.createToken(request);
    }

    // ####################################    Application Service    ########################################

    public ApplicationWorkFlowResponse createApplicationWorkFlow(ApplicationWorkFlowRequest request) {
        return applicationService.createApplicationWorkFlow(request);
    }

    public ApplicationWorkFlowResponse getApplicationWorkFlowById(int id) throws EmployeeNotFoundException {
        return applicationService.getApplicationWorkFlowById(id);
    }

    public List<ApplicationWorkFlowResponse> getAllApplicationWorkFlow() {
        return applicationService.getAllApplicationWorkFlow();
    }

    public ApplicationWorkFlowResponse updateApplicationWorkFlowByEmployeeId(ApplicationWorkFlowRequest request) throws EmployeeNotFoundException {
        return applicationService.updateApplicationWorkFlowByEmployeeId(request);
    }

    public ApplicationWorkFlow getApplicationWorkFlowByEmployeeId(String id) throws EmployeeNotFoundException {
        return applicationService.getApplicationWorkFlowByEmployeeId(id);
    }

    public DigitalDocumentResponse createDigitalDocument(DigitalDocumentRequest request) {
        return applicationService.createDigitalDocument(request);
    }

    public DigitalDocumentResponse getDigitalDocumentById(int id) throws DigitalDocumentNotFoundException {
        return applicationService.getDigitalDocumentById(id);
    }

    public List<DigitalDocumentResponse> getAllDigitalDocument() {
        return applicationService.getAllDigitalDocument();
    }

    // ####################################    Employee Service    ########################################

    public Employee create(EmployeeRequest request) {
        return employeeService.create(request);
    }

    public Employee updateEmployeeById(String id, EmployeeRequest request) throws EmployeeNotFoundException{
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

    public List<Employee> getAllEmployeeInSameHouse(int houseId) {
        return employeeService.getAllEmployeeInSameHouse(String.valueOf(houseId));
    }

    public int getEmployeeHouseIdByEmployeeId(String id) throws EmployeeNotFoundException {
        return employeeService.getEmployeeHouseIdByEmployeeId(id);
    }

    // ####################################    Storage Service    ########################################

    public FileResponse uploadFile(@RequestParam(value = "file") MultipartFile file){
        return storageService.uploadFile(file);
    }

    public ResponseEntity<ByteArrayResource> downloadFile(@PathVariable String fileName) {
        return storageService.downloadFile(fileName);
    }

    public ResponseEntity<String> deleteFile(@PathVariable String fileName) {
        return storageService.deleteFile(fileName);
    }

    // ####################################    Housing Service    ########################################

    public HouseResponse createNewHouse(HouseRequest houseRequest) {
        return housingService.createNewHouse(houseRequest);
    }

    public HouseResponse deleteHouseById(Integer houseId) {
        return housingService.deleteHouseById(houseId);
    }

    public AllHouseResponse getAllHouses() {
        return housingService.getAllHouses();
    }

    public HouseResponse getHouseById(Integer houseId) {
        return housingService.getHouseById(houseId);
    }

    public AllFacilityResponse getAllFacilitiesByHouseId(Integer houseId) {
        return housingService.getAllFacilitiesByHouseId(houseId);
    }

    public AllFacilityReportResponse getAllFacilityReportsByFacilityId(Integer facilityId) {
        return housingService.getAllFacilityReportsByFacilityId(facilityId);
    }

    public FacilityReportResponse getFacilityReportById(Integer facilityReportId) {
        return housingService.getFacilityReportById(facilityReportId);
    }

    public AllFacilityReportDetailResponse getAllFacilityReportDetailByFacilityReportId(Integer FacilityReportId) {
        return housingService.getAllFacilityReportDetailByFacilityReportId(FacilityReportId);
    }

    public FacilityReportDetailResponse createNewFacilityReportDetail(FacilityReportDetailRequest facilityReportDetailRequest) {
        return housingService.createNewFacilityReportDetail(facilityReportDetailRequest);
    }

    public FacilityReportDetailResponse updateFacilityReportDetail(Integer facilityReportDetailID, String employeeID,
                                                                   String newComment) {
        return housingService.updateFacilityReportDetail(facilityReportDetailID, employeeID, newComment);
    }
}
