package com.project.employeeservice.domain.entity;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.web.bind.annotation.RestController;

import java.util.Date;
import java.util.List;

/**
 * @author Guohua Zhang
 * @create 2022-08-15 10:13 AM
 */
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder

@Document
public class Employee {
    @Id
    @ApiModelProperty(notes = "The database generated Employee ID")
    private String id;
    @ApiModelProperty
    private String userId;
    @ApiModelProperty
    private String firstName;
    @ApiModelProperty
    private String lastName;
    @ApiModelProperty
    private String middleName;
    @ApiModelProperty
    private String preferredName;
    @ApiModelProperty
    private String email;
    @ApiModelProperty
    private String cellPhone;
    @ApiModelProperty
    private String alternatePhone;
    @ApiModelProperty
    private String gender;
    @ApiModelProperty
    private String ssn;
    @ApiModelProperty
    private Date dob;
    @ApiModelProperty
    private Date startDate;
    @ApiModelProperty
    private Date endDate;
    @ApiModelProperty
    private String driverLicense;
    @ApiModelProperty
    private Date driverLicenseExpiration;
    @ApiModelProperty
    private String houseID;
    @ApiModelProperty
    private List<Contact> contacts;
    @ApiModelProperty
    private List<Address> addresses;
    @ApiModelProperty
    private List<VisaStatus> visaStatuses;
    @ApiModelProperty
    private List<PersonalDocument> personalDocuments;

}
