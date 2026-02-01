package com.project.emailservice.util;

import com.project.emailservice.domain.message.EmailMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class DeserializeUtil {
    private static ObjectMapper objectMapper = new ObjectMapper();

    public static EmailMessage deserialize(String jsonEmailMessage) {
        EmailMessage result = null;
        try {
            result = objectMapper.readValue(jsonEmailMessage, EmailMessage.class);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }

        return result;
    }
}
