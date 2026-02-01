package com.project.hr.domain.request.application;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class DigitalDocumentRequest {

    private String type;

    private boolean isRequired;

    private String path;

    private String description;

    private String title;
}
