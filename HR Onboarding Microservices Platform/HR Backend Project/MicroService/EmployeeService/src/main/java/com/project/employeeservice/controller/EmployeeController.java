package com.project.employeeservice.controller;

/**
 * @author Guohua Zhang
 * @create 2022-08-15 10:35 PM
 */

import com.project.employeeservice.domain.entity.Employee;
import com.project.employeeservice.domain.request.EmployeeRequest;
import com.project.employeeservice.domain.response.EmployeeVisaInfo;
import com.project.employeeservice.exception.EmployeeNotFoundException;
import com.project.employeeservice.service.EmployeeService;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping
public class EmployeeController {

    private final EmployeeService employeeService;

    @Autowired
    public EmployeeController(EmployeeService employeeService) {
        this.employeeService = employeeService;
    }

    @PostMapping("employee")
    @ApiOperation(value = "Add Employee into DB")
    public Employee create(@RequestBody EmployeeRequest request) {
        return employeeService.create(request);
    }

    @PostMapping("/{id}/update")
    @ApiOperation(value = "Update Employee into DB")
    public Employee updateEmployeeById(@PathVariable String id, @RequestBody EmployeeRequest request) throws EmployeeNotFoundException {
        return employeeService.updateEmployeeById(id, request);
    }

    @GetMapping("/{id}")
    @ApiOperation(value = "Get Employee by Id")
    public Employee getEmployeeById(@PathVariable String id) throws EmployeeNotFoundException {
        return employeeService.getEmployeeById(id);
    }

    @GetMapping
    @ApiOperation(value = "Get All Employee")
    public List<Employee> findAllEmployee() {
        return employeeService.findAllEmployee();
    }

    @GetMapping("/orderByFirstName")
    @ApiOperation(value = "Get All Employee order by first name")
    public List<Employee> findAllEmployeeOrderByFirstNameAsc(){
        return employeeService.findAllEmployeeOrderByFirstNameAsc();
    }

    @GetMapping("/orderByEmail")
    @ApiOperation(value = "Get All Employee order by email")
    public List<Employee> findAllEmployeeOrderByEmailAsc(){
        return employeeService.findAllEmployeeOrderByEmailAsc();
    }

    @GetMapping("/visaInfo")
    @ApiOperation(value = "Get All Employee visa info")
    public List<EmployeeVisaInfo> getAllEmployeeVisaInfo(){
        return employeeService.getAllEmployeeVisaInfo();
    }



    @GetMapping("/house/{houseId}")
    @ApiOperation(value = "Get All Employee living in the same house")
    public List<Employee> getAllEmployeeInSameHouse(@PathVariable String houseId){
        return employeeService.findAllEmployeeInSameHouse(houseId);
    }

    @GetMapping("/{id}/house")
    @ApiOperation(value = "Get Employee HouseId by Employee id")
    public String getEmployeeHouseIdByEmployeeId(@PathVariable String id) throws EmployeeNotFoundException {
        return employeeService.getEmployeeById(id).getHouseID();
    }

    @PostMapping("update")
    @ApiOperation(value = "Update Employee into DB")
    public Employee updateEmployee(Employee e) {
        return employeeService.updateEmployee(e);
    }
}
