package com.project.hr.domain.response.application;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor

public class ApplicationWorkFlow implements Serializable {

    private Integer id;

    private String employeeID;

    private String createDate;

    private String lastModificationDate;

    private String status;

    private String comment;
}
