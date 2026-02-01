package com.project.applicationservice.service;

import com.project.applicationservice.dao.ApplicationWorkFlowDao;
import com.project.applicationservice.domain.entity.ApplicationWorkFlowHibernate;
import com.project.applicationservice.domain.request.ApplicationWorkFlowRequest;
import com.project.applicationservice.domain.response.ApplicationWorkFlowResponse;
import com.project.applicationservice.exception.EmployeeNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;

@Service
public class ApplicationWorkFlowService {

    private final ApplicationWorkFlowDao applicationWorkFlowDao;

    @Autowired
    public ApplicationWorkFlowService(ApplicationWorkFlowDao applicationWorkFlowDao) {
        this.applicationWorkFlowDao = applicationWorkFlowDao;
    }

    @Transactional
    public ApplicationWorkFlowResponse createApplicationWorkFlow(ApplicationWorkFlowRequest request) {
        return applicationWorkFlowDao.createApplicationWorkFlow(request);
    }

    @Transactional
    public ApplicationWorkFlowResponse getApplicationWorkFlowById(int id) throws EmployeeNotFoundException {
        try {
            return applicationWorkFlowDao.getApplicationWorkFlowById(id);
        } catch (Exception e) {
            throw new EmployeeNotFoundException("Employee Not Found");
        }
    }

    @Transactional
    public List<ApplicationWorkFlowResponse> getAllApplicationWorkFlow() {
        return applicationWorkFlowDao.getAllApplicationWorkFlow();
    }

    @Transactional
    public ApplicationWorkFlowResponse updateApplicationWorkFlowById(ApplicationWorkFlowRequest request){
        return applicationWorkFlowDao.updateApplicationWorkFlowById(request);
    }

    @Transactional
    public ApplicationWorkFlowHibernate getApplicationWorkFlowByEmployeeId(String id) throws EmployeeNotFoundException {
        ApplicationWorkFlowHibernate hibA = applicationWorkFlowDao.getApplicationWorkFlowByEmployeeId(id);
        if (hibA == null) {
            throw new EmployeeNotFoundException("Employee Not Found");
        } else {
            return hibA;
        }
    }
}
