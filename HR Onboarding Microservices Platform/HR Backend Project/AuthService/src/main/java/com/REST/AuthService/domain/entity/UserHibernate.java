package com.REST.AuthService.domain.entity;

import lombok.*;

import javax.persistence.*;
import java.io.Serializable;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "User")
public class UserHibernate implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String username;

    private String email;

    private String password;

    private String createDate;

    private String lastModificationDate;

    private boolean activeFlag;

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(name = "UserRole",
            joinColumns = { @JoinColumn(name = "UserId") },
            inverseJoinColumns = { @JoinColumn(name = "RoleId")})
    private List<RoleHibernate> roles;

}

