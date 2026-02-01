package com.project.applicationservice.dao;

import com.project.applicationservice.domain.entity.DigitalDocumentHibernate;
import com.project.applicationservice.domain.request.DigitalDocumentRequest;
import com.project.applicationservice.domain.response.DigitalDocumentResponse;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

@Repository
public class DigitalDocumentDao extends AbstractHibernateDAO<DigitalDocumentHibernate> {

    public DigitalDocumentDao() {
        setClazz(DigitalDocumentHibernate.class);
    }

    public DigitalDocumentResponse createDigitalDocument(DigitalDocumentRequest request) {
        DigitalDocumentHibernate hibD = DigitalDocumentHibernate.builder()
                .type(request.getType())
                .isRequired(request.isRequired())
                .path(request.getPath())
                .description(request.getDescription())
                .title(request.getTitle())
                .build();
        int digitalId = (int) getCurrentSession().save(hibD);

        return buildDigitalDocumentResponse(
                digitalId,
                request.getType(),
                request.isRequired(),
                request.getPath(),
                request.getDescription(),
                request.getTitle());
    }

    public DigitalDocumentResponse getDigitalDocumentById(int id) {
        DigitalDocumentHibernate hibD = findById(id);
        return buildDigitalDocumentResponse(
                hibD.getId(),
                hibD.getType(),
                hibD.isRequired(),
                hibD.getPath(),
                hibD.getDescription(),
                hibD.getTitle());
    }

    public List<DigitalDocumentResponse> getAllDigitalDocument() {
        String query = "from DigitalDocumentHibernate";
        List<DigitalDocumentHibernate> hibDs = getCurrentSession().createQuery(query).getResultList();
        List<DigitalDocumentResponse> responses = new ArrayList<>();

        for (DigitalDocumentHibernate d : hibDs) {
            responses.add(buildDigitalDocumentResponse(
                    d.getId(),
                    d.getType(),
                    d.isRequired(),
                    d.getPath(),
                    d.getDescription(),
                    d.getTitle()
            ));
        }

        return responses;
    }

    private DigitalDocumentResponse buildDigitalDocumentResponse(
            Integer id, String type, boolean isRequired, String path, String description, String title) {
        return DigitalDocumentResponse.builder()
                .id(id)
                .type(type)
                .isRequired(isRequired)
                .path(path)
                .description(description)
                .title(title)
                .build();
    }

}
