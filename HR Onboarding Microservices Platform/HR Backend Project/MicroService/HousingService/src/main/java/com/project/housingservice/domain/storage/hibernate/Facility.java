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
@Table(name="Facility")
@NoArgsConstructor
@AllArgsConstructor
public class Facility implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name="HouseID")
    private House house;

    private String type;

    private String description;

    private Integer quantity;

    @OneToMany(mappedBy = "facility", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JsonIgnore
    private List<FacilityReport> facilityReports;
}
