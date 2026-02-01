package com.project.emailservice.domain.message;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class EmailMessage {
    private String userEmail;
    private String firstname;
    private String lastname;
    private boolean isRejected;
    private String generatedToken;
}
