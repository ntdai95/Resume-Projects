package com.project.housingservice.domain.storage.hibernate;


import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.*;

import javax.persistence.*;
import java.io.Serializable;
import java.util.List;

@Getter
@Setter
@ToString
@Builder
@Entity
@Table(name="FacilityReport")
@NoArgsConstructor
@AllArgsConstructor
public class FacilityReport implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name="FacilityID")
    private Facility facility;

    private String employeeID;

    private String title;

    private String description;

    private String createDate;

    private String status;

    @OneToMany(mappedBy = "facilityReport", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JsonIgnore
    private List<FacilityReportDetail> facilityReportDetails;
}
