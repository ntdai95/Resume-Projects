package com.project.emailservice.listener;

import com.project.emailservice.domain.message.EmailMessage;
import com.project.emailservice.service.EmailService;
import com.project.emailservice.util.DeserializeUtil;

import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageListener;
import org.springframework.beans.factory.annotation.Autowired;

public class RabbitListener implements MessageListener {
    private EmailService emailService;

    @Autowired
    public void setEmailService(EmailService emailService) {
        this.emailService = emailService;
    }

    @Override
    public void onMessage(Message message) {
        EmailMessage emailMessage = DeserializeUtil.deserialize(new String(message.getBody()));
        String emailBody = "Dear " + emailMessage.getFirstname() + " " + emailMessage.getLastname() + ",\n\n";
        String subject = "Application Status";
        if (emailMessage.getGeneratedToken() == null && emailMessage.isRejected()) {
            emailBody += "Unfortunately, your application has been rejected. Please, login to the system to " +
                         "check which field is wrong or if there is any missing document.";
        } else if (emailMessage.getGeneratedToken() == null) {
            emailBody += "Congratulations, your application has been accepted. Welcome onboard!";
        } else {
            subject = "Generated Registration Token";
            emailBody += "The HR has generated the following registration token: " + emailMessage.getGeneratedToken() +
                         " for you to use when you attempt to create your account in the system.";
        }

        emailService.sendSimpleMessage(emailMessage.getUserEmail(), subject, emailBody);
    }
}
