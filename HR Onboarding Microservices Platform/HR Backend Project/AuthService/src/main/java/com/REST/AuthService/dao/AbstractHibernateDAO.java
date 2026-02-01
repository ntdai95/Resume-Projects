package com.REST.AuthService.dao;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.Serializable;

/**
 * abstract class that has common things that a HibernateDAO will need
 * @param <T> generic type for HibernateDAOs
 */
public abstract class AbstractHibernateDAO<T extends Serializable> {

    @Autowired
    protected SessionFactory sessionFactory;

    protected Class<T> clazz;

    protected final void setClazz(final Class<T> clazzToSet) {
        clazz = clazzToSet;
    }

    public T findById(final Integer id) {
        return getCurrentSession().get(clazz, id);
    }

    public void add(T t) {
    	getCurrentSession().persist(t);
    }

    protected Session getCurrentSession() {
        return sessionFactory.getCurrentSession();
    }
}
