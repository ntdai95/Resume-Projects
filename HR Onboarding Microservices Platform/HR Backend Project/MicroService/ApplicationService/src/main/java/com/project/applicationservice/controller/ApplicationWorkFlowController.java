package com.project.applicationservice.controller;

import com.project.applicationservice.domain.entity.ApplicationWorkFlowHibernate;
import com.project.applicationservice.domain.request.ApplicationWorkFlowRequest;
import com.project.applicationservice.domain.response.ApplicationWorkFlowResponse;
import com.project.applicationservice.exception.EmployeeNotFoundException;
import com.project.applicationservice.service.ApplicationWorkFlowService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/workflow")
public class ApplicationWorkFlowController {

    ApplicationWorkFlowService applicationWorkFlowService;

    @Autowired
    public ApplicationWorkFlowController(ApplicationWorkFlowService applicationWorkFlowService) {
        this.applicationWorkFlowService = applicationWorkFlowService;
    }

    @PostMapping("/create")
    public ApplicationWorkFlowResponse createApplicationWorkFlow(@RequestBody ApplicationWorkFlowRequest request) {
        return applicationWorkFlowService.createApplicationWorkFlow(request);
    }

    @GetMapping("/{id}")
    public ApplicationWorkFlowResponse getApplicationWorkFlowById(@PathVariable int id) throws EmployeeNotFoundException {
        return applicationWorkFlowService.getApplicationWorkFlowById(id);
    }

    @GetMapping
    public List<ApplicationWorkFlowResponse> getAllApplicationWorkFlow() {
        return applicationWorkFlowService.getAllApplicationWorkFlow();
    }

    @PostMapping("/update")
    public ApplicationWorkFlowResponse updateApplicationWorkFlowById(@RequestBody ApplicationWorkFlowRequest request) {
        return applicationWorkFlowService.updateApplicationWorkFlowById(request);
    }

    @GetMapping("employee/{id}")
    public ApplicationWorkFlowHibernate getApplicationWorkFlowByEmployeeId(@PathVariable String id) throws EmployeeNotFoundException {
        return applicationWorkFlowService.getApplicationWorkFlowByEmployeeId(id);
    }

}
