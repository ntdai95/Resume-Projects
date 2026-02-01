package com.project.housingservice.domain.storage.hibernate;

import lombok.*;

import javax.persistence.*;
import java.io.Serializable;

@Getter
@Setter
@ToString
@Builder
@Entity
@Table(name="FacilityReportDetail")
@NoArgsConstructor
@AllArgsConstructor
public class FacilityReportDetail implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name="FacilityReportID")
    private FacilityReport facilityReport;

    private String employeeID;

    private String comment;

    private String createDate;

    private String lastModificationDate;
}
