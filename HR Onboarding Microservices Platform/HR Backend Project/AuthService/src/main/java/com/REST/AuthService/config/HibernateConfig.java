package com.REST.AuthService.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.orm.hibernate5.HibernateTransactionManager;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;
import java.util.Properties;

@Configuration
@EnableTransactionManagement
public class HibernateConfig {

	HibernateProperty hibernateProperty;

	@Autowired
	public void setHibernateProperty(HibernateProperty hibernateProperty) {
		this.hibernateProperty = hibernateProperty;
	}

	@Bean
	protected LocalSessionFactoryBean sessionFactory() {
		LocalSessionFactoryBean sessionFactory = new LocalSessionFactoryBean();
		sessionFactory.setDataSource(dataSource());
		sessionFactory.setPackagesToScan("com.REST.AuthService.domain");
		sessionFactory.setHibernateProperties(hibernateProperties());

		return sessionFactory;
	}

	@Bean
	public DataSource dataSource() {
		DriverManagerDataSource dataSource = new DriverManagerDataSource();
		dataSource.setDriverClassName(hibernateProperty.getDriver());
		dataSource.setUrl(hibernateProperty.getUrl());
		dataSource.setUsername(hibernateProperty.getUsername());
		dataSource.setPassword(hibernateProperty.getPassword());
		return dataSource;
	}

	@Bean
	public PlatformTransactionManager hibernateTransactionManager() {
		HibernateTransactionManager transactionManager = new HibernateTransactionManager();
		transactionManager.setSessionFactory(sessionFactory().getObject());
		return transactionManager;
	}

	private final Properties hibernateProperties() {
		Properties hibernateProperties = new Properties();
		hibernateProperties.setProperty("hibernate.show_sql", hibernateProperty.getShowsql());
		hibernateProperties.setProperty("hibernate.dialect", hibernateProperty.getDialect());
		hibernateProperties.setProperty("hibernate.hbm2ddl.auto", hibernateProperty.getHbm2ddl());
		return hibernateProperties;
	}
}
