package com.project.onboard.controller;

import com.project.onboard.domain.request.application.ApplicationWorkFlowRequest;
import com.project.onboard.domain.request.employee.*;
import com.project.onboard.domain.request.housing.FacilityReportDetailRequest;
import com.project.onboard.domain.request.housing.FacilityReportRequest;
import com.project.onboard.domain.request.user.RegisterUserRequest;
import com.project.onboard.domain.response.application.ApplicationWorkFlowResponse;
import com.project.onboard.domain.response.employee.*;
import com.project.onboard.domain.response.housing.*;
import com.project.onboard.domain.response.storage.FileResponse;
import com.project.onboard.domain.response.user.DigitalDocumentResponse;
import com.project.onboard.domain.response.user.RegisterUserResponse;
import com.project.onboard.entity.FacilityReport;
import com.project.onboard.entity.FacilityReportDetail;
import com.project.onboard.exception.*;
import com.project.onboard.service.OnboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;

@RestController
public class OnboardController {

    private final OnboardService onboardService;

    private final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    @Autowired
    public OnboardController(OnboardService onboardService) {
        this.onboardService = onboardService;
    }

    // ####################################    User Service    ########################################

    @PostMapping("/register")
    public RegisterUserResponse registerUser(@RequestBody RegisterUserRequest request, @RequestParam String token) {
        try {
            return onboardService.registerUser(request, token);
        } catch (Exception e) {
            throw new BadCredentialsException(e.getMessage());
        }
    }

    // ####################################    Application Service    ########################################

    @GetMapping("application/{id}")
    public ApplicationWorkFlowResponse getApplicationWorkFlowById(@PathVariable String id) throws EmployeeNotFoundException {
        try {
            return onboardService.getApplicationWorkFlowById(id);
        } catch(Exception e) {
            throw new EmployeeNotFoundException(e.getMessage());
        }
    }

    // ####################################    House Service    ########################################

    @GetMapping(value = "/house/{houseId}")
    public HouseDetailPageResponse getHouseDetailPageByHouseId(@PathVariable Integer houseId) throws HouseNotFoundException {
        if (houseId < 1) { throw new RuntimeException("Invalid house ID."); }

        try {
            HouseResponse houseResponse = onboardService.getHouseDetailPageByHouseId(houseId);
            List<Employee> employees = onboardService.getAllEmployeeInSameHouse(String.valueOf(houseId));

            return HouseDetailPageResponse.builder()
                    .address(houseResponse.getHouse().getAddress())
                    .employees(employees)
                    .build();
        } catch (Exception e) {
            throw new HouseNotFoundException(e.getMessage());
        }
    }

    @PostMapping(value = "/facilityReport")
    public FacilityReportResponse createNewFacilityReport(@RequestBody FacilityReportRequest facilityReportRequest) throws FacilityNotFoundException {
        try {
            return onboardService.createNewFacilityReport(facilityReportRequest);
        } catch (Exception e) {
            throw new FacilityNotFoundException(e.getMessage());
        }
    }

    @GetMapping(value = "/facilityReport")
    public AllFacilityReportResponse getAllFacilityReports() throws FacilityReportNotFoundException {
        try {
            AllFacilityReportResponse allFacilityReportResponse = onboardService.getAllFacilityReports();
            if (allFacilityReportResponse.getFacilityReports() != null) {
                for (FacilityReport facilityReport : allFacilityReportResponse.getFacilityReports()) {
                    facilityReport.setFacility(null);
                    if (facilityReport.getFacilityReportDetails() != null) {
                        for (FacilityReportDetail facilityReportDetail : facilityReport.getFacilityReportDetails()) {
                            facilityReportDetail.setId(null);
                            facilityReportDetail.setCreateDate(null);
                        }
                    } else {
                        AllFacilityReportDetailResponse allFacilityReportDetailResponse = onboardService.getAllFacilityReportDetailByFacilityReportId(facilityReport.getId());
                        if (allFacilityReportDetailResponse.getFacilityReportDetails() != null) {
                            for (FacilityReportDetail facilityReportDetail : allFacilityReportDetailResponse.getFacilityReportDetails()) {
                                facilityReportDetail.setFacilityReport(null);
                                facilityReportDetail.setCreateDate(null);
                            }
                            facilityReport.setFacilityReportDetails(allFacilityReportDetailResponse.getFacilityReportDetails());
                        }
                    }
                    facilityReport.setId(null);
                }
            }

            return allFacilityReportResponse;
        } catch (Exception e) {
            throw new FacilityReportNotFoundException(e.getMessage());
        }
    }

    @PostMapping(value = "/facilityReportDetail")
    public FacilityReportDetailResponse createNewFacilityReportDetail(@RequestBody FacilityReportDetailRequest facilityReportDetailRequest) throws FacilityReportNotFoundException {
        try {
            return onboardService.createNewFacilityReportDetail(facilityReportDetailRequest);
        } catch (Exception e) {
            throw new FacilityReportNotFoundException(e.getMessage());
        }
    }

    @GetMapping(value = "/facilityReportDetail/{facilityReportId}")
    public AllFacilityReportDetailResponse getAllFacilityReportDetailByFacilityReportId(@PathVariable Integer facilityReportId) throws FacilityReportDetailNotFoundException {
        if (facilityReportId < 1) {
            throw new RuntimeException("Invalid facility report ID.");
        }

        try {
            AllFacilityReportDetailResponse allFacilityReportDetailResponse = onboardService.getAllFacilityReportDetailByFacilityReportId(facilityReportId);
            if (allFacilityReportDetailResponse.getFacilityReportDetails() != null) {
                for (FacilityReportDetail facilityReportDetail : allFacilityReportDetailResponse.getFacilityReportDetails()) {
                    facilityReportDetail.setFacilityReport(null);
                    facilityReportDetail.setCreateDate(null);
                }
            }

            return allFacilityReportDetailResponse;
        } catch (Exception e) {
            throw new FacilityReportDetailNotFoundException(e.getMessage());
        }
    }

    @PatchMapping(value = "/facilityReportDetail/{facilityReportDetailID}")
    public FacilityReportDetailResponse updateFacilityReportDetail(@PathVariable Integer facilityReportDetailID,
                                                                   @RequestParam String employeeID, @RequestParam String newComment) throws FacilityReportDetailNotFoundException {
        if (facilityReportDetailID < 1) {
            throw new RuntimeException("Invalid facility report detail ID.");
        }

        try {
            return onboardService.updateFacilityReportDetail(facilityReportDetailID, employeeID, newComment);
        } catch (Exception e) {
            throw new FacilityReportDetailNotFoundException(e.getMessage());
        }
    }

    // ####################################    Employee Service    ########################################

    String downloadPath = "http://localhost:9000/onboard/user/file/download/";

    @GetMapping("user/{id}")
    public Employee getEmployeeById(@PathVariable String id) throws EmployeeNotFoundException {
        return onboardService.getEmployeeById(id);
    }

    @GetMapping("user/DigitalDocuments")
    public List<DigitalDocumentResponse> getAllDigitalDocument() {
        return onboardService.getAllDigitalDocument();
    }

    @GetMapping("user/file/download/{fileName}")
    public ResponseEntity<ByteArrayResource> downloadFile(@PathVariable String fileName) {
        return onboardService.downloadFile(fileName);
    }

    @PostMapping("user/{id}/file/upload")
    public FileResponse uploadFile(@RequestPart(value = "file") MultipartFile file, @PathVariable String id) throws EmployeeNotFoundException {
        FileResponse response = onboardService.uploadFile(file);

        Employee e = onboardService.getEmployeeById(id);
        List<PersonalDocument> personalDocuments = e.getPersonalDocuments();
        personalDocuments.add(PersonalDocument.builder()
                .path(downloadPath + response.getFileStatus())
                .title(response.getFileStatus())
                .comment(response.getFileStatus() + "document")
                .createDate(new java.util.Date())
                .build());
        e.setPersonalDocuments(personalDocuments);
        onboardService.updateEmployeeById(e.getId(), buildEmployeeRequest(e));

        return response;
    }

    @PostMapping("user/submitApplication")
    public Employee submitApplication(@RequestPart(value = "request") EmployeeRequest request,
                                      @RequestPart(value = "permanent") Optional<MultipartFile> permanent,
                                      @RequestPart(value = "visa") Optional<MultipartFile> visa,
                                      @RequestPart(value = "driverLicense") Optional<MultipartFile> driverLicense,
                                      @RequestPart(value = "digitalDocuments") List<MultipartFile> digitalDocuments) {
        List<PersonalDocumentRequest> documents = new ArrayList<>();
        if (permanent.isPresent()) {
            FileResponse response = onboardService.uploadFile(permanent.get());
            documents.add(PersonalDocumentRequest.builder()
                            .path(downloadPath + response.getFileStatus())
                            .title(response.getFileStatus())
                            .comment(response.getFileStatus() + "document")
                            .createDate(new java.util.Date())
                    .build());
        } else if (visa.isPresent()) {
            FileResponse response = onboardService.uploadFile(visa.get());
            documents.add(PersonalDocumentRequest.builder()
                    .path(downloadPath + response.getFileStatus())
                    .title(response.getFileStatus())
                    .comment(response.getFileStatus() + "document")
                    .createDate(new java.util.Date())
                    .build());
        }

        if (driverLicense.isPresent()) {
            FileResponse response = onboardService.uploadFile(driverLicense.get());
            request.setDriverLicense(downloadPath + response.getFileStatus());
            documents.add(PersonalDocumentRequest.builder()
                    .path(downloadPath + response.getFileStatus())
                    .title(response.getFileStatus())
                    .comment(response.getFileStatus() + "document")
                    .createDate(new java.util.Date())
                    .build());
        }

        for (MultipartFile file : digitalDocuments) {
            FileResponse response = onboardService.uploadFile(file);
            documents.add(PersonalDocumentRequest.builder()
                    .path(downloadPath + response.getFileStatus())
                    .title(response.getFileStatus())
                    .comment(response.getFileStatus() + "document")
                    .createDate(new java.util.Date())
                    .build());
        }
        request.setPersonalDocuments(documents);
        Employee e = onboardService.create(request);
        ApplicationWorkFlowRequest workFlowRequest = ApplicationWorkFlowRequest.builder()
                .employeeID(e.getId())
                .createDate(LocalDateTime.now().format(formatter))
                .lastModificationDate(LocalDateTime.now().format(formatter))
                .status("Pending")
                .comment(" ")
                .build();
        onboardService.createApplicationWorkFlow(workFlowRequest);

        return e;
    }

    @PostMapping("user/{id}/update")
    public Employee updateEmployeeById(@PathVariable String id, @RequestBody EmployeeRequest request) throws EmployeeNotFoundException {
        return onboardService.updateEmployeeById(id, request);
    }

    @GetMapping("user/{id}/activeVisa")
    public VisaStatus getActiveVisaByEmployeeId(@PathVariable String id) throws EmployeeNotFoundException {
        Employee e = onboardService.getEmployeeById(id);
        for (VisaStatus v : e.getVisaStatuses()) {
            if (v.getActiveFlag()) {
                return v;
            }
        }
        return null;
    }

    @PostMapping("user/{id}/updateVisa")
    public Employee updateVisaByEmployeeId(@PathVariable String id, @RequestBody VisaStatusRequest request) throws EmployeeNotFoundException {
        Employee e = onboardService.getEmployeeById(id);
        System.out.println(e);
        List<VisaStatus> visaStatuses = e.getVisaStatuses();
        for (VisaStatus v : visaStatuses) {
            if (v.getActiveFlag()) {
                visaStatuses.remove(v);
                v.setActiveFlag(false);
                visaStatuses.add(v);
            }
        }
        visaStatuses.add(VisaStatus.builder()
                        .visaType(request.getVisaType())
                        .activeFlag(request.getActiveFlag())
                        .startDate(request.getStartDate())
                        .endDate(request.getEndDate())
                        .lastModificationDate(new java.util.Date()).build());
        e.setVisaStatuses(visaStatuses);

        return onboardService.updateEmployeeById(e.getId(), buildEmployeeRequest(e));
    }

    @GetMapping("user/{id}/documents")
    public List<PersonalDocument> getAllPersonalDocumentByEmployeeId(@PathVariable String id) throws EmployeeNotFoundException {
        Employee e = onboardService.getEmployeeById(id);
        return e.getPersonalDocuments();
    }

    public EmployeeRequest buildEmployeeRequest(Employee employee) {
        List<ContactRequest> contacts = new ArrayList<>();
        for (Contact c: employee.getContacts()) {
            contacts.add(buildContact(c));
        }
        List<AddressRequest> addresses = new ArrayList<>();
        for (Address a : employee.getAddresses()) {
            addresses.add(buildAddress(a));
        }
        List<VisaStatusRequest> visaStatuses = new ArrayList<>();
        for(VisaStatus v : employee.getVisaStatuses()) {
            visaStatuses.add(buildVisaStatus(v));
        }
        List<PersonalDocumentRequest> personalDocuments = new ArrayList<>();
        for(PersonalDocument p : employee.getPersonalDocuments()) {
            personalDocuments.add(buildPersonalDocument(p));
        }

        return EmployeeRequest.builder()
                .userId(employee.getUserId())
                .firstName(employee.getFirstName())
                .lastName(employee.getLastName())
                .middleName(employee.getMiddleName())
                .preferredName(employee.getPreferredName())
                .email(employee.getEmail())
                .cellPhone(employee.getCellPhone())
                .alternatePhone(employee.getAlternatePhone())
                .gender(employee.getGender())
                .ssn(employee.getSsn())
                .dob(employee.getDob())
                .startDate(employee.getStartDate())
                .endDate(employee.getEndDate())
                .driverLicense(employee.getDriverLicense())
                .driverLicenseExpiration(employee.getDriverLicenseExpiration())
                .houseId(employee.getHouseID())
                .contacts(contacts)
                .addresses(addresses)
                .visaStatuses(visaStatuses)
                .personalDocuments(personalDocuments)
                .build();
    }

    public ContactRequest buildContact(Contact contact) {
        return ContactRequest.builder()
                .firstName(contact.getFirstName())
                .lastName(contact.getLastName())
                .cellPhone(contact.getCellPhone())
                .alternatePhone(contact.getAlternatePhone())
                .email(contact.getEmail())
                .relationship(contact.getRelationship())
                .type(contact.getType())
                .build();
    }

    public AddressRequest buildAddress(Address request) {
        return AddressRequest.builder()
                .addressLine1(request.getAddressLine1())
                .addressLine2(request.getAddressLine2())
                .city(request.getCity())
                .state(request.getState())
                .zipCode(request.getZipCode())
                .build();
    }

    public VisaStatusRequest buildVisaStatus(VisaStatus request) {
        return VisaStatusRequest.builder()
                .visaType(request.getVisaType())
                .activeFlag(request.getActiveFlag())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .lastModificationDate(request.getLastModificationDate())
                .build();
    }

    public PersonalDocumentRequest buildPersonalDocument(PersonalDocument request) {
        return PersonalDocumentRequest.builder()
                .path(request.getPath())
                .title(request.getTitle())
                .comment(request.getComment())
                .createDate(request.getCreateDate())
                .build();
    }

}
