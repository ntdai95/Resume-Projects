package com.project.onboard.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;

import java.util.List;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Landlord {
    private Integer id;

    private String firstName;

    private String lastName;

    private String email;

    private String cellPhone;

    private List<House> houses;
}
