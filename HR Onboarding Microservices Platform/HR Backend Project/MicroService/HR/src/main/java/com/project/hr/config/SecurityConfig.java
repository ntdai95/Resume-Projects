package com.project.hr.config;

import com.project.hr.domain.security.JwtFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatus;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.builders.WebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    private JwtFilter jwtFilter;

    @Autowired
    public void setJwtFilter(JwtFilter jwtFilter) {
        this.jwtFilter = jwtFilter;
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                .csrf().disable()
                .addFilterAfter(jwtFilter, UsernamePasswordAuthenticationFilter.class)
                .authorizeRequests()
//                .antMatchers("/manage", "/manage/*").permitAll()
//                .antMatchers(HttpMethod.GET, "/user", "/user/info/*").hasAuthority("read")
                .antMatchers("/hr/registrationToken").hasAuthority("HR")
                .antMatchers("/hr/*").hasAnyAuthority("HR","User")
//                .antMatchers(HttpMethod.PATCH, "/user/*/status").hasAuthority("update")
//                .antMatchers(HttpMethod.DELETE,"/user").hasAuthority("delete")
                .anyRequest()
                .authenticated()
                .and().exceptionHandling().authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED));

    }
    @Override
    public void configure(WebSecurity web) throws Exception {
        web
                .ignoring()
                .antMatchers("/hr/register");
    }
}
