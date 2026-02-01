package com.project.applicationservice.service;

import com.project.applicationservice.dao.DigitalDocumentDao;
import com.project.applicationservice.domain.request.DigitalDocumentRequest;
import com.project.applicationservice.domain.response.DigitalDocumentResponse;
import com.project.applicationservice.exception.DigitalDocumentNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;

@Service
public class DigitalDocumentService {

    final DigitalDocumentDao digitalDocumentDao;

    @Autowired
    public DigitalDocumentService(DigitalDocumentDao digitalDocumentDao) {
        this.digitalDocumentDao = digitalDocumentDao;
    }

    @Transactional
    public DigitalDocumentResponse createDigitalDocument(DigitalDocumentRequest request) {
        return digitalDocumentDao.createDigitalDocument(request);
    }

    @Transactional
    public DigitalDocumentResponse getDigitalDocumentById(int id) throws DigitalDocumentNotFoundException {
        try {
            return digitalDocumentDao.getDigitalDocumentById(id);
        } catch (Exception e) {
            throw new DigitalDocumentNotFoundException("Document not found");
        }
    }

    @Transactional
    public List<DigitalDocumentResponse> getAllDigitalDocument() {
        return digitalDocumentDao.getAllDigitalDocument();
    }
}
