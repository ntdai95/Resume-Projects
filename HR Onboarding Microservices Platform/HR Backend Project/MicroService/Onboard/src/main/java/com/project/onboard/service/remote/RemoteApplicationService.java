package com.project.onboard.service.remote;

import com.project.onboard.domain.request.application.ApplicationWorkFlowRequest;
import com.project.onboard.domain.response.application.ApplicationWorkFlowResponse;
import com.project.onboard.domain.response.user.DigitalDocumentResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;

@FeignClient("application")
public interface RemoteApplicationService {

    @GetMapping("application/workflow/{id}")
    ApplicationWorkFlowResponse getApplicationWorkFlowById(@PathVariable String id);

    @GetMapping("application/digitalDoc")
    List<DigitalDocumentResponse> getAllDigitalDocument();

    @PostMapping("application/workflow/create")
    ApplicationWorkFlowResponse createApplicationWorkFlow(@RequestBody ApplicationWorkFlowRequest request);
}
