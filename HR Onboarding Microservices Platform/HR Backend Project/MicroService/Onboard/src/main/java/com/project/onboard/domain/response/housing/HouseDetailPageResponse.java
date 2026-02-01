package com.project.onboard.domain.response.housing;

import com.project.onboard.domain.response.employee.Employee;
import lombok.*;

import java.util.List;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class HouseDetailPageResponse {
    private String address;

    private List<Employee> employees;
}
