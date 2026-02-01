package com.project.onboard.service.remote;

import com.project.onboard.domain.request.employee.EmployeeRequest;
import com.project.onboard.domain.response.employee.Employee;
import com.project.onboard.domain.response.employee.EmployeeVisaInfo;
import com.project.onboard.exception.EmployeeNotFoundException;
import io.swagger.annotations.ApiOperation;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;

@FeignClient("employee")
public interface RemoteEmployeeService {
    @PostMapping("employee")
    @ApiOperation(value = "Add Employee into DB")
    Employee create(@RequestBody EmployeeRequest request);

    @PostMapping("employee/{id}/update")
    @ApiOperation(value = "Update Employee into DB")
    Employee updateEmployeeById(@PathVariable String id, @RequestBody EmployeeRequest request) throws EmployeeNotFoundException;

    @GetMapping("employee/{id}")
    @ApiOperation(value = "Get Employee by Id")
    Employee getEmployeeById(@PathVariable String id) throws EmployeeNotFoundException;

    @GetMapping("employee")
    @ApiOperation(value = "Get All Employee")
    List<Employee> findAllEmployee();

    @GetMapping("employee/orderByFirstName")
    @ApiOperation(value = "Get All Employee order by first name")
    List<Employee> findAllEmployeeOrderByFirstNameAsc();

    @GetMapping("employee/orderByEmail")
    @ApiOperation(value = "Get All Employee order by email")
    List<Employee> findAllEmployeeOrderByEmailAsc();

    @GetMapping("employee/visaInfo")
    @ApiOperation(value = "Get All Employee visa info")
    List<EmployeeVisaInfo> getAllEmployeeVisaInfo();

    @GetMapping("employee/house/{houseId}")
    @ApiOperation(value = "Get All Employee living in the same house")
    List<Employee> getAllEmployeeInSameHouse(@PathVariable String houseId);

    @GetMapping("employee/{id}/house")
    @ApiOperation(value = "Get Employee HouseId by Employee id")
    String getEmployeeHouseIdByEmployeeId(@PathVariable String id) throws EmployeeNotFoundException;

    @PostMapping("employee/update")
    @ApiOperation(value = "update Employee into DB")
    Employee updateEmployee(Employee e);
}
