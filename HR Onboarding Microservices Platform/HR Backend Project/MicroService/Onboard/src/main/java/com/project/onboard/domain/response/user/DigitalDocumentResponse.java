package com.project.onboard.domain.response.user;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class DigitalDocumentResponse {
    private Integer id;

    private String type;

    private boolean isRequired;

    private String path;

    private String description;

    private String title;
}
