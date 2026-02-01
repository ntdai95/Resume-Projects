package com.project.onboard.domain.response.employee;

import io.swagger.annotations.ApiModelProperty;
import lombok.*;

import java.util.Date;
import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Employee {
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
