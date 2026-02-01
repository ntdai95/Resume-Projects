package com.project.userservice.dao;


import com.project.userservice.domain.entity.RegistrationTokenHibernate;
import com.project.userservice.domain.entity.UserHibernate;
import com.project.userservice.domain.entity.UserRoleHibernate;
import com.project.userservice.domain.request.RegistrationToken;
import com.project.userservice.domain.request.RegisterUserRequest;
import com.project.userservice.domain.response.RegistrationTokenResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Random;

@Repository
@PropertySource("classpath:application.properties")
public class UserDao extends AbstractHibernateDAO<UserHibernate> {

    @Value("${tokenExpirationHour}")
    private int expirationHour;

    private final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

//    public Optional<UserHibernate> loadUserByUsername(String credential) throws BadCredentialsException {
//        String userQuery = "from UserHibernate where username =:credential or email =:credential";
//        UserHibernate hibU = (UserHibernate) getCurrentSession()
//                .createQuery(userQuery)
//                .setParameter("credential", credential)
//                .getSingleResult();
////        System.out.println(hibU);
//        return Optional.of(hibU);
//    }
//
//    public List<GrantedAuthority> getAuthoritiesFromUser(UserHibernate user){
//        System.out.println("get authorities in dao");
//        String permissionsQuery = "from UserHibernate u join fetch u.roles where u.id =:userId";
//        UserHibernate hibU = (UserHibernate) getCurrentSession()
//                .createQuery(permissionsQuery)
//                .setParameter("userId", user.getId()).getSingleResult();
//        List<GrantedAuthority> userAuthorities = new ArrayList<>();
//
//        for (RoleHibernate role : hibU.getRoles()) {
//            userAuthorities.add(new SimpleGrantedAuthority(role.getRoleName()));
//        }
//
//        return userAuthorities;
//    }

    public RegistrationTokenResponse createRegistrationToken(RegistrationToken request) {
        String allUserQuery = "from UserHibernate";
        List<UserHibernate> hibUs = getCurrentSession().createQuery(allUserQuery).getResultList();
        for (UserHibernate u : hibUs) {
            System.out.println(u);
        }
        String userQuery = "from UserHibernate where id =: id";
        // TODO Should I call another service or this is okay
        UserHibernate hibU = (UserHibernate) getCurrentSession().createQuery(userQuery)
                .setParameter("id", request.getCreateBy()).getSingleResult();
        System.out.println(hibU);
        String generatedString = generateToken();
        System.out.println(generatedString);
        // TODO Change this to using RabbitMQ

        LocalDateTime time = LocalDateTime.parse(request.getExpirationDate(), formatter).plusHours(expirationHour);
        System.out.println(time);
        RegistrationTokenHibernate hibT = RegistrationTokenHibernate.builder()
                .token(generatedString)
                .email(request.getUserEmail())
                .expirationDate(time.format(formatter))
                .user(hibU).build();
        hibT.setId((Integer) getCurrentSession().save(hibT));

        return RegistrationTokenResponse.builder()
                .id(hibT.getId())
                .token(hibT.getToken())
                .email(hibT.getEmail())
                .expirationDate(hibT.getExpirationDate())
                .build();
    }

    public int registerUser(RegisterUserRequest request, String token) {
        String tokenQuery = "from RegistrationTokenHibernate where email =: email";
        RegistrationTokenHibernate hibT;
        try {
            hibT = (RegistrationTokenHibernate) getCurrentSession().createQuery(tokenQuery)
                    .setParameter("email", request.getEmail()).getSingleResult();
        } catch (Exception e) {
            throw new BadCredentialsException("Please contact HR about Token");
        }

        String userQuery = "from UserHibernate where email =: email";
        try {
            getCurrentSession().createQuery(userQuery).setParameter("email", request.getEmail()).getSingleResult();
            throw new BadCredentialsException("Account with the same Email already exists, contact HR");
        } catch (BadCredentialsException e) {
            throw new BadCredentialsException(e.getMessage());
        } catch (Exception e) {
            // do nothing because no account with email exists which is good.
        }

        if (LocalDateTime.now().isAfter(LocalDateTime.parse(hibT.getExpirationDate(), formatter))) {
            throw new BadCredentialsException("You are past the registration time, contact HR");
        } else if (!hibT.getToken().equals(token)) {
            throw new BadCredentialsException("Make sure your token is valid");
        }  else {
            UserHibernate hibU = UserHibernate.builder()
                    .username(request.getUsername())
                    .email(request.getEmail())
                    .password(request.getPassword())
                    .createDate(LocalDateTime.now().format(formatter))
                    .lastModificationDate(LocalDateTime.now().format(formatter))
                    .activeFlag(true).build();
            int userId = (int) getCurrentSession().save(hibU);

            UserRoleHibernate hibUR = UserRoleHibernate.builder()
                    .userId(userId)
                    .roleId(1)
                    .activeFlag(true)
                    .createDate(LocalDateTime.now().format(formatter))
                    .lastModificationDate(LocalDateTime.now().format(formatter)).build();
            getCurrentSession().save(hibUR);

            return userId;
        }
    }

    /**
     * Taken from link: <a href="https://www.baeldung.com/java-random-string">...</a> #5
     * @return random generated token with target length of 20
     */
    private String generateToken() {
        int leftLimit = 48; // numeral '0'
        int rightLimit = 122; // letter 'z'
        int targetStringLength = 20;
        Random random = new Random();

        return random.ints(leftLimit, rightLimit + 1)
                .filter(i -> (i <= 57 || i >= 65) && (i <= 90 || i >= 97))
                .limit(targetStringLength)
                .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
                .toString();
    }
}
