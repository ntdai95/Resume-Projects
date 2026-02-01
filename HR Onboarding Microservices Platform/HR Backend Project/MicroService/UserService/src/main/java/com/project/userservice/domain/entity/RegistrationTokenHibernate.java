package com.project.userservice.domain.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "RegistrationToken")
public class RegistrationTokenHibernate {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String token;

    private String email;

    private String expirationDate;

    @ManyToOne
    @JoinColumn(name = "CreateBy")
    private UserHibernate user;
}
