package com.REST.AuthService.service;

import com.REST.AuthService.dao.UserDao;
import com.REST.AuthService.domain.entity.UserHibernate;
import com.REST.AuthService.domain.security.AuthUserDetail;
import com.REST.AuthService.exception.UserNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;
import java.util.Optional;

@Service
public class UserService implements UserDetailsService {

    private UserDao userDao;

    @Autowired
    public void setUserDao(UserDao userDao) {
        this.userDao = userDao;
    }

    @Transactional
    @Override
    public UserDetails loadUserByUsername(String credential) throws BadCredentialsException {
        Optional<UserHibernate> userOptional = userDao.loadUserByUsername(credential);

        if (!userOptional.isPresent()){
            throw new UsernameNotFoundException("Username does not exist");
        }

        UserHibernate user = userOptional.get();
//        System.out.println("user: "+user);
//        System.out.println("permissions: "+ getAuthoritiesFromUser(user));
        return AuthUserDetail.builder() // spring security's userDetail
                .username(user.getUsername())
                .password(new BCryptPasswordEncoder().encode(user.getPassword()))
                .authorities(getAuthoritiesFromUser(user))
                .accountNonExpired(true)
                .accountNonLocked(true)
                .credentialsNonExpired(true)
                .enabled(true)
                .build();
    }

    @Transactional
    List<GrantedAuthority> getAuthoritiesFromUser(UserHibernate user){
        return userDao.getAuthoritiesFromUser(user);
    }
}
