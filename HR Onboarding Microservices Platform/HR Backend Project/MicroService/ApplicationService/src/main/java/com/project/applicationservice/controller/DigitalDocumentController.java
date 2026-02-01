package com.project.applicationservice.controller;

import com.project.applicationservice.domain.request.DigitalDocumentRequest;
import com.project.applicationservice.domain.response.DigitalDocumentResponse;
import com.project.applicationservice.exception.DigitalDocumentNotFoundException;
import com.project.applicationservice.service.DigitalDocumentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/digitalDoc")
public class DigitalDocumentController {

    final DigitalDocumentService digitalDocumentService;

    @Autowired
    public DigitalDocumentController(DigitalDocumentService digitalDocumentService) {
        this.digitalDocumentService = digitalDocumentService;
    }

    @PostMapping("/create")
    public DigitalDocumentResponse createDigitalDocument(@RequestBody DigitalDocumentRequest request){
        return digitalDocumentService.createDigitalDocument(request);
    }

    @GetMapping("/{id}")
    public DigitalDocumentResponse getDigitalDocumentById(@PathVariable int id) throws DigitalDocumentNotFoundException {
        return digitalDocumentService.getDigitalDocumentById(id);
    }

    @GetMapping
    public List<DigitalDocumentResponse> getAllDigitalDocument() {
        return digitalDocumentService.getAllDigitalDocument();
    }

}
