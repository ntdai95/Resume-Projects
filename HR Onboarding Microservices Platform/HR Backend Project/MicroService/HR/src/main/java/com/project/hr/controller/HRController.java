package com.project.hr.controller;

import com.project.hr.domain.request.application.ApplicationWorkFlowRequest;
import com.project.hr.domain.request.application.DigitalDocumentRequest;
import com.project.hr.domain.request.email.EmailMessage;
import com.project.hr.domain.request.employee.EmployeeRequest;
import com.project.hr.domain.request.housing.FacilityReportDetailRequest;
import com.project.hr.domain.request.housing.HouseRequest;
import com.project.hr.domain.request.registration.RegistrationToken;
import com.project.hr.domain.response.application.ApplicationWorkFlowResponse;
import com.project.hr.domain.response.application.DigitalDocumentResponse;
import com.project.hr.domain.response.employee.Employee;
import com.project.hr.domain.response.employee.EmployeeVisaInfo;
import com.project.hr.domain.response.housing.*;
import com.project.hr.domain.response.registration.RegistrationTokenResponse;
import com.project.hr.entity.Facility;
import com.project.hr.entity.FacilityReport;
import com.project.hr.entity.FacilityReportDetail;
import com.project.hr.entity.House;
import com.project.hr.exception.*;
import com.project.hr.service.HRService;
import com.project.hr.util.ObjectSerializeUtil;
import io.swagger.annotations.ApiOperation;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class HRController {

    private final HRService hrService;

    private final RabbitTemplate rabbitTemplate;

    @Autowired
    public HRController(HRService hrService, RabbitTemplate rabbitTemplate) {
        this.hrService = hrService;
        this.rabbitTemplate = rabbitTemplate;
    }

    // ####################################    Features    ########################################
    @GetMapping("home/activeVisa")
    @ApiOperation(value = "Get All Employee visa info")
    public List<EmployeeVisaInfo> getAllEmployeeVisaInfo(){
        return hrService.getAllEmployeeVisaInfo();
    }

    @GetMapping("employeeProfile")
    @ApiOperation(value = "Get All Employee")
    public List<Employee> getAllEmployee(){
        return hrService.findAllEmployee();
    }

    @GetMapping("employeeProfile/orderByFirstName")
    @ApiOperation(value = "Get All Employee order by first name")
    public List<Employee> getAllEmployeeOrderByFirstNameAsc(){
        return hrService.findAllEmployeeOrderByFirstNameAsc();
    }

    @GetMapping("employeeProfile/orderByEmail")
    @ApiOperation(value = "Get All Employee order by email")
    public List<Employee> getAllEmployeeOrderByEmailAsc(){
        return hrService.findAllEmployeeOrderByEmailAsc();
    }

    @PostMapping("hire/registrationToken")
    public RegistrationTokenResponse createTokenAndSendEmail(@RequestBody RegistrationToken request){
        RegistrationTokenResponse token = hrService.createToken(request);
        EmailMessage emailMessage = EmailMessage.builder()
                .userEmail("jjpan3418@gmail.com")
                .firstname("Bobby")
                .lastname("Pop")
                .generatedToken(token.getToken())
                .build();

        String jsonUserOrderResponse = ObjectSerializeUtil.serialize(emailMessage);
        rabbitTemplate.convertAndSend("emailExchange", "emailKey", jsonUserOrderResponse);

        return token;
    }

    @GetMapping("application")
    public List<ApplicationWorkFlowResponse> getAllApplicationWorkFlow() {
        return hrService.getAllApplicationWorkFlow();
    }

    @GetMapping("application/{id}")
    public Employee getEmployeeApplicationWorkFlow(@PathVariable int id) throws EmployeeNotFoundException {
        ApplicationWorkFlowResponse response = hrService.getApplicationWorkFlowById(id);
        return hrService.getEmployeeById(response.getEmployeeID());
    }

    @GetMapping("application/{employeeId}/file/download/{fileName}")
    public ResponseEntity<ByteArrayResource> downloadFile(@PathVariable String fileName, @PathVariable String employeeId) {
        return hrService.downloadFile(fileName);
    }

    @PostMapping("application/workflow/update")
    public ApplicationWorkFlowResponse updateApplicationWorkFlowByEmployeeId(@RequestBody ApplicationWorkFlowRequest request) throws EmployeeNotFoundException {
        try {
            EmailMessage emailMessage = null;
            if (request.getStatus().equals("Completed")) {
                emailMessage = EmailMessage.builder()
                        .userEmail(request.getEmail())
                        .firstname(request.getFirstName())
                        .lastname(request.getLastName())
                        .isRejected(false)
                        .build();
            } else if (request.getStatus().equals("Rejected")) {
                emailMessage = EmailMessage.builder()
                        .userEmail(request.getEmail())
                        .firstname(request.getFirstName())
                        .lastname(request.getLastName())
                        .isRejected(true)
                        .build();
            }

            String jsonUserOrderResponse = ObjectSerializeUtil.serialize(emailMessage);
            rabbitTemplate.convertAndSend("emailExchange", "emailKey", jsonUserOrderResponse);

            return hrService.updateApplicationWorkFlowByEmployeeId(request);

        } catch (EmployeeNotFoundException e) {
            throw new EmployeeNotFoundException(e.getMessage());
        }
    }


    // ####################################    User Service    ########################################
    @PostMapping("/registrationToken")
    public RegistrationTokenResponse createToken(@RequestBody RegistrationToken request){
        return hrService.createToken(request);
    }

    // ####################################    Application Service    ########################################

    @PostMapping("workflow/create")
    public ApplicationWorkFlowResponse createApplicationWorkFlow(@RequestBody ApplicationWorkFlowRequest request) {
        return hrService.createApplicationWorkFlow(request);
    }

    @GetMapping("workflow/{id}")
    public ApplicationWorkFlowResponse getApplicationWorkFlowById(@PathVariable int id) throws EmployeeNotFoundException {
        try {
            return hrService.getApplicationWorkFlowById(id);
        } catch (EmployeeNotFoundException e) {
            throw new EmployeeNotFoundException(e.getMessage());
        }
    }

//    @GetMapping("workflow")
//    public List<ApplicationWorkFlowResponse> getAllApplicationWorkFlow() {
//        return hrService.getAllApplicationWorkFlow();
//    }

//    @PostMapping("workflow/update")
//    public ApplicationWorkFlowResponse updateApplicationWorkFlowByEmployeeId(@RequestBody ApplicationWorkFlowRequest request) throws EmployeeNotFoundException {
//        try {
//            return hrService.updateApplicationWorkFlowByEmployeeId(request);
//        } catch (EmployeeNotFoundException e) {
//            throw new EmployeeNotFoundException(e.getMessage());
//        }
//    }

    @PostMapping("digitalDoc/create")
    public DigitalDocumentResponse createDigitalDocument(@RequestBody DigitalDocumentRequest request){
        return hrService.createDigitalDocument(request);
    }

    @GetMapping("digitalDoc/{id}")
    public DigitalDocumentResponse getDigitalDocumentById(@PathVariable int id) throws DigitalDocumentNotFoundException {
        try {
            return hrService.getDigitalDocumentById(id);
        } catch (DigitalDocumentNotFoundException e) {
            throw new DigitalDocumentNotFoundException(e.getMessage());
        }
    }

    @GetMapping("digitalDoc")
    public List<DigitalDocumentResponse> getAllDigitalDocument() {
        return hrService.getAllDigitalDocument();
    }

    // ####################################    Employee Service    ########################################

    @PostMapping("employee")
    @ApiOperation(value = "Add Employee into DB")
    public Employee create(@RequestBody EmployeeRequest request) {
        return hrService.create(request);
    }

    @PostMapping("employee/{id}/update")
    @ApiOperation(value = "Update Employee into DB")
    public Employee updateEmployeeById(@PathVariable String id, @RequestBody EmployeeRequest request) throws EmployeeNotFoundException {
        return hrService.updateEmployeeById(id, request);
    }

    @GetMapping("employee/{id}")
    @ApiOperation(value = "Get Employee by Id")
    public Employee getEmployeeById(@PathVariable String id) throws EmployeeNotFoundException {
        return hrService.getEmployeeById(id);
    }

//    @GetMapping("employee/orderByFirstName")
//    @ApiOperation(value = "Get All Employee order by first name")
//    public List<Employee> findAllEmployeeOrderByFirstNameAsc(){
//        return hrService.findAllEmployeeOrderByFirstNameAsc();
//    }
//
//    @GetMapping("employee/orderByEmail")
//    @ApiOperation(value = "Get All Employee order by email")
//    public List<Employee> findAllEmployeeOrderByEmailAsc(){
//        return hrService.findAllEmployeeOrderByEmailAsc();
//    }

//    @GetMapping("employee/visaInfo")
//    @ApiOperation(value = "Get All Employee visa info")
//    public List<EmployeeVisaInfo> getAllEmployeeVisaInfo(){
//        return hrService.getAllEmployeeVisaInfo();
//    }

    @GetMapping("employee/house/{houseId}")
    @ApiOperation(value = "Get All Employee living in the same house")
    public List<Employee> getAllEmployeeInSameHouse(@PathVariable int houseId){
        return hrService.getAllEmployeeInSameHouse(houseId);
    }

    @GetMapping("employee/{id}/house")
    @ApiOperation(value = "Get Employee HouseId by Employee id")
    public String getEmployeeHouseIdByEmployeeId(@PathVariable String id) throws EmployeeNotFoundException {
        return hrService.getEmployeeById(id).getHouseID();
    }

    // ####################################    Housing Service    ########################################


    @PostMapping(value = "house")
    public HouseResponse createNewHouse(@RequestBody HouseRequest houseRequest) throws LandlordNotFoundException {
        try {
            return hrService.createNewHouse(houseRequest);
        } catch (Exception e) {
            throw new LandlordNotFoundException(e.getMessage());
        }
    }

    @DeleteMapping(value = "house/{houseId}")
    public HouseResponse deleteHouseById(@PathVariable Integer houseId) throws HouseNotFoundException {
        if (houseId < 1) {
            throw new RuntimeException("Invalid house ID.");
        }

        try {
            return hrService.deleteHouseById(houseId);
        } catch (Exception e) {
            throw new HouseNotFoundException(e.getMessage());
        }
    }

    @GetMapping(value = "house")
    public AllHouseResponse getAllHouses() throws HouseNotFoundException {
        try {
            AllHouseResponse allHouseResponse = hrService.getAllHouses();
            if (allHouseResponse.getHouses() != null) {
                for (House house : allHouseResponse.getHouses()) {
                    house.setId(null);
                    if (house.getLandlord() != null) {
                        house.getLandlord().setId(null);
                        house.getLandlord().setHouses(null);
                    }
                    house.setFacilities(null);
                }
            }

            return allHouseResponse;
        } catch (Exception e) {
            throw new HouseNotFoundException(e.getMessage());
        }
    }

    @GetMapping(value = "house/{houseId}")
    public HouseResponse getHouseById(@PathVariable Integer houseId) throws HouseNotFoundException {
        if (houseId < 1) {
            throw new RuntimeException("Invalid house ID.");
        }

        try {
            HouseResponse houseResponse = hrService.getHouseById(houseId);
            if (houseResponse.getHouse() != null) {
                if (houseResponse.getHouse().getLandlord() != null) {
                    houseResponse.getHouse().getLandlord().setId(null);
                    houseResponse.getHouse().getLandlord().setHouses(null);
                }
                houseResponse.getHouse().setMaxOccupant(null);
                List<Employee> employees = hrService.getAllEmployeeInSameHouse(houseId);
                houseResponse.getHouse().setCurrentEmployeeCount(employees.size());

                if (houseResponse.getHouse().getFacilities() != null) {
                    for (Facility facility : houseResponse.getHouse().getFacilities()) {
                        facility.setHouse(null);
                        if (facility.getFacilityReports() != null) {
                            for (FacilityReport facilityReport : facility.getFacilityReports()) {
                                facilityReport.setFacility(null);
                                facilityReport.setEmployeeID(null);
                                facilityReport.setDescription(null);
                                facilityReport.setFacilityReportDetails(null);
                            }
                        } else {
                            AllFacilityReportResponse allFacilityReportResponse = hrService.getAllFacilityReportsByFacilityId(facility.getId());
                            if (allFacilityReportResponse.getFacilityReports() != null) {
                                for (FacilityReport facilityReport : allFacilityReportResponse.getFacilityReports()) {
                                    facilityReport.setFacility(null);
                                    facilityReport.setEmployeeID(null);
                                    facilityReport.setDescription(null);
                                    facilityReport.setFacilityReportDetails(null);
                                }
                            }
                            facility.setFacilityReports(allFacilityReportResponse.getFacilityReports());
                        }
                        facility.setId(null);
                    }
                } else {
                    AllFacilityResponse allFacilityResponse = hrService.getAllFacilitiesByHouseId(houseResponse.getHouse().getId());
                    if (allFacilityResponse.getFacilities() != null) {
                        for (Facility facility : allFacilityResponse.getFacilities()) {
                            facility.setHouse(null);
                            if (facility.getFacilityReports() != null) {
                                for (FacilityReport facilityReport : facility.getFacilityReports()) {
                                    facilityReport.setFacility(null);
                                    facilityReport.setEmployeeID(null);
                                    facilityReport.setDescription(null);
                                    facilityReport.setFacilityReportDetails(null);
                                }
                            } else {
                                AllFacilityReportResponse allFacilityReportResponse = hrService.getAllFacilityReportsByFacilityId(facility.getId());
                                if (allFacilityReportResponse.getFacilityReports() != null) {
                                    for (FacilityReport facilityReport : allFacilityReportResponse.getFacilityReports()) {
                                        facilityReport.setFacility(null);
                                        facilityReport.setEmployeeID(null);
                                        facilityReport.setDescription(null);
                                        facilityReport.setFacilityReportDetails(null);
                                    }
                                }
                                facility.setFacilityReports(allFacilityReportResponse.getFacilityReports());
                            }
                            facility.setId(null);
                        }
                    }
                    houseResponse.getHouse().setFacilities(allFacilityResponse.getFacilities());
                }
                houseResponse.getHouse().setId(null);
            }

            return houseResponse;
        } catch (Exception e) {
            throw new HouseNotFoundException(e.getMessage());
        }
    }

    @GetMapping(value = "/facilityReport/byFacilityReportId/{facilityReportId}")
    public FacilityReportResponse getFacilityReportById(@PathVariable Integer facilityReportId) throws FacilityReportNotFoundException {
        if (facilityReportId < 1) {
            throw new RuntimeException("Invalid facility report ID.");
        }

        try {
            FacilityReportResponse facilityReportResponse = hrService.getFacilityReportById(facilityReportId);
            if (facilityReportResponse.getFacilityReport() != null) {
                facilityReportResponse.getFacilityReport().setFacility(null);
                facilityReportResponse.getFacilityReport().setEmployeeID(null);
                if (facilityReportResponse.getFacilityReport().getFacilityReportDetails() != null) {
                    for (FacilityReportDetail facilityReportDetail : facilityReportResponse.getFacilityReport().getFacilityReportDetails()) {
                        facilityReportDetail.setId(null);
                        facilityReportDetail.setFacilityReport(null);
                        facilityReportDetail.setCreateDate(null);
                    }
                } else {
                    AllFacilityReportDetailResponse allFacilityReportDetailResponse = hrService.getAllFacilityReportDetailByFacilityReportId(facilityReportResponse.getFacilityReport().getId());
                    if (allFacilityReportDetailResponse.getFacilityReportDetails() != null) {
                        for (FacilityReportDetail facilityReportDetail : allFacilityReportDetailResponse.getFacilityReportDetails()) {
                            facilityReportDetail.setId(null);
                            facilityReportDetail.setFacilityReport(null);
                            facilityReportDetail.setCreateDate(null);
                        }
                    }
                    facilityReportResponse.getFacilityReport().setFacilityReportDetails(allFacilityReportDetailResponse.getFacilityReportDetails());
                }
                facilityReportResponse.getFacilityReport().setId(null);
            }

            return facilityReportResponse;
        } catch (Exception e) {
            throw new FacilityReportNotFoundException(e.getMessage());
        }
    }

    @PostMapping(value = "/facilityReportDetail")
    public FacilityReportDetailResponse createNewFacilityReportDetail(@RequestBody FacilityReportDetailRequest facilityReportDetailRequest) throws FacilityReportNotFoundException {
        try {
            return hrService.createNewFacilityReportDetail(facilityReportDetailRequest);
        } catch (Exception e) {
            throw new FacilityReportNotFoundException(e.getMessage());
        }
    }

    @PatchMapping(value = "/facilityReportDetail/{facilityReportDetailID}")
    public FacilityReportDetailResponse updateFacilityReportDetail(@PathVariable Integer facilityReportDetailID,
                                                                   @RequestParam String employeeID, @RequestParam String newComment) throws FacilityReportDetailNotFoundException {
        if (facilityReportDetailID < 1) {
            throw new RuntimeException("Invalid facility report detail ID.");
        }

        try {
            return hrService.updateFacilityReportDetail(facilityReportDetailID, employeeID, newComment);
        } catch (Exception e) {
            throw new FacilityReportDetailNotFoundException(e.getMessage());
        }
    }
}
