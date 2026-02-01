package com.project.hr.service.remote;

import com.project.hr.domain.request.application.ApplicationWorkFlowRequest;
import com.project.hr.domain.request.application.DigitalDocumentRequest;
import com.project.hr.domain.response.application.ApplicationWorkFlow;
import com.project.hr.domain.response.application.ApplicationWorkFlowResponse;
import com.project.hr.domain.response.application.DigitalDocumentResponse;
import com.project.hr.exception.DigitalDocumentNotFoundException;
import com.project.hr.exception.EmployeeNotFoundException;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;

@FeignClient("application")
public interface RemoteApplicationService {

    @PostMapping("application/workflow/create")
    ApplicationWorkFlowResponse createApplicationWorkFlow(@RequestBody ApplicationWorkFlowRequest request);

    @GetMapping("application/workflow/{id}")
    ApplicationWorkFlowResponse getApplicationWorkFlowById(@PathVariable int id)  throws EmployeeNotFoundException ;

    @GetMapping("application/workflow")
    List<ApplicationWorkFlowResponse> getAllApplicationWorkFlow();

    @PostMapping("application/workflow/update")
    ApplicationWorkFlowResponse updateApplicationWorkFlowByEmployeeId(@RequestBody ApplicationWorkFlowRequest request) throws EmployeeNotFoundException;

    @GetMapping("application/workflow/employee/{id}")
    ApplicationWorkFlow getApplicationWorkFlowByEmployeeId(@PathVariable String id) throws EmployeeNotFoundException;

    @PostMapping("application/digitalDoc/create")
    DigitalDocumentResponse createDigitalDocument(@RequestBody DigitalDocumentRequest request);

    @GetMapping("application/digitalDoc/{id}")
    DigitalDocumentResponse getDigitalDocumentById(@PathVariable int id) throws DigitalDocumentNotFoundException;

    @GetMapping("application/digitalDoc")
    List<DigitalDocumentResponse> getAllDigitalDocument();
}