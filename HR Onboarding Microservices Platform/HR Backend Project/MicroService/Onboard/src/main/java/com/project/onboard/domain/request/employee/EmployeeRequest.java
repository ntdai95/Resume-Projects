package com.project.onboard.domain.request.employee;

import lombok.*;

import java.util.Date;
import java.util.List;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class EmployeeRequest {

    private String userId;
    private String firstName;
    private String lastName;
    private String middleName;
    private String preferredName;
    private String email;
    private String cellPhone;
    private String alternatePhone;
    private String gender;
    private String ssn;
    private Date dob;
    private Date startDate;
    private Date endDate;
    private String driverLicense;
    private Date driverLicenseExpiration;
    private String houseId;
    private List<ContactRequest> contacts;
    private List<AddressRequest> addresses;
    private List<VisaStatusRequest> visaStatuses;
    private List<PersonalDocumentRequest> personalDocuments;
}
