package com.project.employeeservice.service;

import com.project.employeeservice.domain.entity.*;
import com.project.employeeservice.domain.request.*;
import com.project.employeeservice.domain.response.EmployeeVisaInfo;
import com.project.employeeservice.exception.EmployeeNotFoundException;
import com.project.employeeservice.repository.EmployeeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.bson.types.ObjectId;


import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.TimeUnit;

/**
 * @author Guohua Zhang
 * @create 2022-08-15 10:52 PM
 */

@Service
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    @Autowired
    public EmployeeService(EmployeeRepository employeeRepository) {
        this.employeeRepository = employeeRepository;
    }
    public Employee create(EmployeeRequest request) {
        return employeeRepository.save(buildEmployee(request));
    }

    public Employee updateEmployeeById(String id, EmployeeRequest request) throws EmployeeNotFoundException {
        Employee e = buildEmployee(request);
        e.setId(id);
        return employeeRepository.save(e);
    }

    public Employee getEmployeeById(String id) throws EmployeeNotFoundException {

        Optional<Employee> e = employeeRepository.findById(id);
        if (e.isPresent()) {
            return e.get();
        } else {
            throw new EmployeeNotFoundException("Employee not found");
        }
    }

    public List<Employee> findAllEmployee() {
        return employeeRepository.findAll();
    }

    public List<Employee> findAllEmployeeOrderByFirstNameAsc() {
        return employeeRepository.findAllByOrderByFirstNameAsc();
    }

    public List<Employee> findAllEmployeeOrderByEmailAsc() {
        return employeeRepository.findAllByOrderByEmailAsc();
    }

    public List<Employee> findAllEmployeeInSameHouse(String houseId){
        return employeeRepository.findAllByHouseID(houseId);
    }

    public List<EmployeeVisaInfo> getAllEmployeeVisaInfo(){
        List<Employee> employees = employeeRepository.findAll();
        List<EmployeeVisaInfo> employeeVisaInfoList = new ArrayList<>();
        for (Employee e : employees) {
            String fullName = e.getFirstName();
            if (e.getMiddleName() != null) {
                fullName = fullName + " " + e.getMiddleName();
            }
            fullName += " " + e.getLastName();
            VisaStatus activeVisa = null;
            for (VisaStatus v : e.getVisaStatuses()) {
                if (v.getActiveFlag()) {
                    activeVisa = v;
                }
            }
            assert activeVisa != null;
            employeeVisaInfoList.add(buildEmployeeVisaInfo(e.getId(), fullName, activeVisa));
        }
        return employeeVisaInfoList;
    }

    public Employee updateEmployee(Employee e) {
        System.out.println(e);
        return employeeRepository.save(e);
    }

    private EmployeeVisaInfo buildEmployeeVisaInfo(String id, String fullName, VisaStatus activeVisa){
        Date end = activeVisa.getEndDate();
        long millis=System.currentTimeMillis();
        Date current = new Date(millis);
        long time_difference = end.getTime() - current.getTime();
        System.out.println();
        if (time_difference < 0) {
            time_difference = 0;
        }
        long daysLeft = TimeUnit.MILLISECONDS.toDays(time_difference) % 365;
        return EmployeeVisaInfo.builder()
                .employeeId(id)
                .name(fullName)
                .workAuthorization(activeVisa.getVisaType())
                .expirationDate(activeVisa.getEndDate())
                .dateLeft((int) daysLeft)
                .build();
    }

    public Employee buildEmployee(EmployeeRequest request) {
        List<Contact> contacts = new ArrayList<>();
        for (ContactRequest c: request.getContacts()) {
            contacts.add(buildContact(c));
        }
        List<Address> addresses = new ArrayList<>();
        for (AddressRequest a : request.getAddresses()) {
            addresses.add(buildAddress(a));
        }
        List<VisaStatus> visaStatuses = new ArrayList<>();
        for(VisaStatusRequest v : request.getVisaStatuses()) {
            visaStatuses.add(buildVisaStatus(v));
        }
        List<PersonalDocument> personalDocuments = new ArrayList<>();
        for(PersonalDocumentRequest p : request.getPersonalDocuments()) {
            personalDocuments.add(buildPersonalDocument(p));
        }

        return Employee.builder()
                .userId(request.getUserId())
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .middleName(request.getMiddleName())
                .preferredName(request.getPreferredName())
                .email(request.getEmail())
                .cellPhone(request.getCellPhone())
                .alternatePhone(request.getAlternatePhone())
                .gender(request.getGender())
                .ssn(request.getSsn())
                .dob(request.getDob())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .driverLicense(request.getDriverLicense())
                .driverLicenseExpiration(request.getDriverLicenseExpiration())
                .houseID(request.getHouseId())
                .contacts(contacts)
                .addresses(addresses)
                .visaStatuses(visaStatuses)
                .personalDocuments(personalDocuments)
                .build();
    }

    public Contact buildContact(ContactRequest request) {
        return Contact.builder()
                .id(String.valueOf(new ObjectId()))
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .cellPhone(request.getCellPhone())
                .alternatePhone(request.getAlternatePhone())
                .email(request.getEmail())
                .relationship(request.getRelationship())
                .type(request.getType())
                .build();
    }

    public Address buildAddress(AddressRequest request) {
        return Address.builder()
                .id(String.valueOf(new ObjectId()))
                .addressLine1(request.getAddressLine1())
                .addressLine2(request.getAddressLine2())
                .city(request.getCity())
                .state(request.getState())
                .zipCode(request.getZipCode())
                .build();
    }

    public VisaStatus buildVisaStatus(VisaStatusRequest request) {
        return VisaStatus.builder()
                .id(String.valueOf(new ObjectId()))
                .visaType(request.getVisaType())
                .activeFlag(request.getActiveFlag())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .lastModificationDate(request.getLastModificationDate())
                .build();
    }

    public PersonalDocument buildPersonalDocument(PersonalDocumentRequest request) {
        return PersonalDocument.builder()
                .id(String.valueOf(new ObjectId()))
                .path(request.getPath())
                .title(request.getTitle())
                .comment(request.getComment())
                .createDate(request.getCreateDate())
                .build();
    }
}
