package com.REST.AuthService.dao;


import com.REST.AuthService.domain.entity.RoleHibernate;
import com.REST.AuthService.domain.entity.UserHibernate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Repository;

import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
@PropertySource("classpath:application.properties")
public class UserDao extends AbstractHibernateDAO<UserHibernate>{

    public Optional<UserHibernate> loadUserByUsername(String credential) throws BadCredentialsException {
        String userQuery = "from UserHibernate where username =:credential or email =:credential";
        UserHibernate hibU = (UserHibernate) getCurrentSession()
                .createQuery(userQuery)
                .setParameter("credential", credential)
                .getSingleResult();
//        System.out.println(hibU);
        return Optional.of(hibU);
    }

    public List<GrantedAuthority> getAuthoritiesFromUser(UserHibernate user){
        System.out.println("get authorities in dao");
        String permissionsQuery = "from UserHibernate u join fetch u.roles where u.id =:userId";
        UserHibernate hibU = (UserHibernate) getCurrentSession()
                .createQuery(permissionsQuery)
                .setParameter("userId", user.getId()).getSingleResult();
        List<GrantedAuthority> userAuthorities = new ArrayList<>();

        for (RoleHibernate role : hibU.getRoles()) {
            userAuthorities.add(new SimpleGrantedAuthority(role.getRoleName()));
        }

        return userAuthorities;
    }

}
