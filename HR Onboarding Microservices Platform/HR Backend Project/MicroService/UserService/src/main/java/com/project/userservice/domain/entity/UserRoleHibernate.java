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
@Table(name = "UserRole")
public class UserRoleHibernate {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private int userId;

    private int roleId;

    private boolean activeFlag;

    private String createDate;

    private String lastModificationDate;

    @Override
    public String toString() {
        return "UserRoleHibernate{" +
                "id=" + id +
                ", userId=" + userId +
                ", roleId=" + roleId +
                ", activeFlag=" + activeFlag +
                ", createDate='" + createDate + '\'' +
                ", lastModificationDate='" + lastModificationDate + '\'' +
                '}';
    }
}
