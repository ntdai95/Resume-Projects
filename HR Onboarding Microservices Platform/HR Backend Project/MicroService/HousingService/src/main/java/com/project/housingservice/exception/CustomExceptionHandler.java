package com.project.housingservice.exception;

import com.project.housingservice.domain.response.Error.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class CustomExceptionHandler {
    @ExceptionHandler(value = {RuntimeException.class})
    public ResponseEntity handleInvalidHouseIdException(Exception e) {
        return new ResponseEntity(ErrorResponse.builder().message(e.getMessage()).build(), HttpStatus.OK);
    }

    @ExceptionHandler(value = {HouseNotFoundException.class})
    public ResponseEntity<ErrorResponse> handleHouseNotFoundException(HouseNotFoundException e) {
        return new ResponseEntity(ErrorResponse.builder().message(e.getMessage()).build(), HttpStatus.OK);
    }

    @ExceptionHandler(value = {FacilityReportNotFoundException.class})
    public ResponseEntity<ErrorResponse> handleFacilityReportNotFoundException(FacilityReportNotFoundException e) {
        return new ResponseEntity(ErrorResponse.builder().message(e.getMessage()).build(), HttpStatus.OK);
    }

    @ExceptionHandler(value = {FacilityReportDetailNotFoundException.class})
    public ResponseEntity<ErrorResponse> handleFacilityReportDetailNotFoundException(FacilityReportDetailNotFoundException e) {
        return new ResponseEntity(ErrorResponse.builder().message(e.getMessage()).build(), HttpStatus.OK);
    }

    @ExceptionHandler(value = {LandlordNotFoundException.class})
    public ResponseEntity<ErrorResponse> handleLandlordNotFoundException(LandlordNotFoundException e) {
        return new ResponseEntity(ErrorResponse.builder().message(e.getMessage()).build(), HttpStatus.OK);
    }

    @ExceptionHandler(value = {FacilityNotFoundException.class})
    public ResponseEntity<ErrorResponse> handleFacilityNotFoundException(FacilityNotFoundException e) {
        return new ResponseEntity(ErrorResponse.builder().message(e.getMessage()).build(), HttpStatus.OK);
    }
}
