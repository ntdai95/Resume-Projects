package com.project.employeeservice.repository;

import com.project.employeeservice.domain.entity.Employee;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;
import java.util.Optional;


public interface EmployeeRepository extends MongoRepository<Employee, String> {
    Optional<Employee> findById(String id);

    List<Employee> findAllByOrderByFirstNameAsc();

    List<Employee> findAllByOrderByEmailAsc();

    List<Employee> findAllByHouseID(String id);
}

