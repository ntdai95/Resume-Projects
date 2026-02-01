package com.project.hr.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ObjectSerializeUtil {

    private static ObjectMapper objectMapper = new ObjectMapper();

    public static <T> String serialize(T object){

        String result = null;

        try {
            result = objectMapper.writeValueAsString(object);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }

        return result;
    }
}
