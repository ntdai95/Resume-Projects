package com.project.userservice.service;

import com.project.userservice.dao.UserDao;
import com.project.userservice.domain.entity.RegistrationTokenHibernate;
import com.project.userservice.domain.request.RegistrationToken;
import com.project.userservice.domain.request.RegisterUserRequest;
import com.project.userservice.domain.response.RegistrationTokenResponse;
import com.project.userservice.exception.UserNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;

@Service
public class UserService { //implements UserDetailsService

    private UserDao userDao;

    @Autowired
    public void setUserDao(UserDao userDao) {
        this.userDao = userDao;
    }

//    @Transactional
//    @Override
//    public UserDetails loadUserByUsername(String credential) throws BadCredentialsException {
//        Optional<UserHibernate> userOptional = userDao.loadUserByUsername(credential);
//
//        if (!userOptional.isPresent()){
//            throw new UsernameNotFoundException("Username does not exist");
//        }
//
//        UserHibernate user = userOptional.get();
////        System.out.println("user: "+user);
////        System.out.println("permissions: "+ getAuthoritiesFromUser(user));
//        return AuthUserDetail.builder() // spring security's userDetail
//                .username(user.getUsername())
//                .password(new BCryptPasswordEncoder().encode(user.getPassword()))
//                .authorities(getAuthoritiesFromUser(user))
//                .accountNonExpired(true)
//                .accountNonLocked(true)
//                .credentialsNonExpired(true)
//                .enabled(true)
//                .build();
//    }
//
//    @Transactional
//    List<GrantedAuthority> getAuthoritiesFromUser(UserHibernate user){
//        return userDao.getAuthoritiesFromUser(user);
//    }

    @Transactional
    public RegistrationTokenResponse createRegistrationToken(RegistrationToken request) throws UserNotFoundException {
        try {
            return userDao.createRegistrationToken(request);
        } catch (Exception e) {
            System.out.println(e);
            throw new UserNotFoundException("User not found");
        }
    }

    @Transactional
    public int registerUser(RegisterUserRequest request, String token) {

        return userDao.registerUser(request, token);
    }
}
