package com.project.applicationservice.dao;

import com.project.applicationservice.domain.entity.ApplicationWorkFlowHibernate;
import com.project.applicationservice.domain.request.ApplicationWorkFlowRequest;
import com.project.applicationservice.domain.response.ApplicationWorkFlowResponse;
import com.project.applicationservice.exception.EmployeeNotFoundException;
import org.hibernate.Criteria;
import org.hibernate.criterion.Restrictions;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

@Repository
public class ApplicationWorkFlowDao extends AbstractHibernateDAO<ApplicationWorkFlowHibernate> {

    private final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public ApplicationWorkFlowDao() {
        setClazz(ApplicationWorkFlowHibernate.class);
    }

    public ApplicationWorkFlowResponse createApplicationWorkFlow(ApplicationWorkFlowRequest request) {
        ApplicationWorkFlowHibernate hibA = ApplicationWorkFlowHibernate.builder()
                .employeeID(request.getEmployeeID())
                .createDate(request.getCreateDate())
                .lastModificationDate(request.getLastModificationDate())
                .status(request.getStatus())
                .comment(request.getComment())
                .build();
        return applicationWorkFlowResponseBuilder(
                (Integer) getCurrentSession().save(hibA),
                request.getEmployeeID(),
                request.getCreateDate(),
                request.getLastModificationDate(),
                request.getStatus(),
                request.getComment());
    }

    public ApplicationWorkFlowResponse getApplicationWorkFlowById(int id) {
        String query = "from ApplicationWorkFlowHibernate where id =: id";
        ApplicationWorkFlowHibernate hibA = (ApplicationWorkFlowHibernate) getCurrentSession().createQuery(query)
                .setParameter("id", id).getSingleResult();
        return applicationWorkFlowResponseBuilder(
                (Integer) getCurrentSession().save(hibA),
                hibA.getEmployeeID(),
                hibA.getCreateDate(),
                hibA.getLastModificationDate(),
                hibA.getStatus(),
                hibA.getComment());
    }

    public List<ApplicationWorkFlowResponse> getAllApplicationWorkFlow() {
        String query = "from ApplicationWorkFlowHibernate";
        List<ApplicationWorkFlowHibernate> hibAList = getCurrentSession().createQuery(query).getResultList();
        List<ApplicationWorkFlowResponse> resultList = new ArrayList<>();
        for (ApplicationWorkFlowHibernate a : hibAList) {
            resultList.add(applicationWorkFlowResponseBuilder(
                    a.getId(),
                    a.getEmployeeID(),
                    a.getCreateDate(),
                    a.getLastModificationDate(),
                    a.getStatus(),
                    a.getComment()
            ));
        }
        return resultList;
    }

    public ApplicationWorkFlowResponse updateApplicationWorkFlowById(ApplicationWorkFlowRequest request) {

        String query = "from ApplicationWorkFlowHibernate where id =: id";
        ApplicationWorkFlowHibernate hibA = (ApplicationWorkFlowHibernate) getCurrentSession().createQuery(query)
                .setParameter("id", request.getId()).getSingleResult();

        hibA.setLastModificationDate(LocalDateTime.now().format(formatter));
        hibA.setStatus(request.getStatus());
        hibA.setComment(request.getComment());
        getCurrentSession().save(hibA);

        return applicationWorkFlowResponseBuilder(
                hibA.getId(),
                hibA.getEmployeeID(),
                hibA.getCreateDate(),
                hibA.getLastModificationDate(),
                hibA.getStatus(),
                hibA.getComment());
    }

    public ApplicationWorkFlowHibernate getApplicationWorkFlowByEmployeeId(String id) {
        Criteria criteria = getCurrentSession().createCriteria(ApplicationWorkFlowHibernate.class);
        criteria.add(Restrictions.ne("status","Completed"));
        criteria.add(Restrictions.eq("employeeID", id));
        ApplicationWorkFlowHibernate hibA = null;
        try {
            hibA = (ApplicationWorkFlowHibernate) criteria.list().get(0);
        } catch (Exception e) {
//            throw new EmployeeNotFoundException("Employee Not Found");
        }
        return hibA;
    }

    private ApplicationWorkFlowResponse applicationWorkFlowResponseBuilder(
            int id, String employeeID, String createDate, String lastModificationDate, String status, String comment){
        return ApplicationWorkFlowResponse.builder()
                .id(id)
                .employeeID(employeeID)
                .createDate(createDate)
                .lastModificationDate(lastModificationDate)
                .status(status)
                .comment(comment)
                .build();
    }

}
