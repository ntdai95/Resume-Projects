package com.project.housingservice.controller;

import com.project.housingservice.domain.request.House.HouseRequest;
import com.project.housingservice.domain.response.House.AllHouseResponse;
import com.project.housingservice.domain.response.House.HouseResponse;
import com.project.housingservice.domain.storage.hibernate.House;
import com.project.housingservice.exception.HouseNotFoundException;
import com.project.housingservice.exception.LandlordNotFoundException;
import com.project.housingservice.service.HouseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
@RestController
@RequestMapping(value = "house")
public class HouseController {
    private HouseService houseService;

    @Autowired
    public void setHousingService(HouseService houseService) {
        this.houseService = houseService;
    }

    @GetMapping(value = "{houseId}")
    public ResponseEntity<HouseResponse> getHouseById(@PathVariable Integer houseId) throws HouseNotFoundException {
        if (houseId < 1) { throw new RuntimeException("Invalid house ID."); }

        House house = houseService.getHouseById(houseId);
        if (house == null) {
            throw new HouseNotFoundException("The house with the id of " + houseId + " does not exist.");
        }

        return ResponseEntity.ok(HouseResponse.builder()
                                              .message("Returning house with the id of " + houseId)
                                              .house(house)
                                              .build());
    }

    @PostMapping
    public ResponseEntity<HouseResponse> createNewHouse(@RequestBody HouseRequest houseRequest) throws LandlordNotFoundException {
        int houseID = houseService.createNewHouse(houseRequest);
        if (houseID == -1) {
            throw new LandlordNotFoundException("The landlord with the id of " + houseRequest.getLandlordID() + " does not exist.");
        }

        return ResponseEntity.ok(HouseResponse.builder()
                                              .message("New house with the id of " + houseID + " has been created.")
                                              .build());
    }

    @DeleteMapping(value = "{houseId}")
    public ResponseEntity<HouseResponse> deleteHouseById(@PathVariable Integer houseId) throws HouseNotFoundException {
        if (houseId < 1) {
            throw new RuntimeException("Invalid house ID.");
        }

        boolean isHouseExist = houseService.deleteHouseById(houseId);
        if (!isHouseExist) {
            throw new HouseNotFoundException("The house with the id of " + houseId + " does not exist.");
        }

        return ResponseEntity.ok(HouseResponse.builder()
                                              .message("House with the id of " + houseId + " has been deleted.")
                                              .build());
    }

    @GetMapping
    public ResponseEntity<AllHouseResponse> getAllHouses() throws HouseNotFoundException {
        List<House> houseList = houseService.getAllHouses();
        if (houseList.size() == 0) {
            throw new HouseNotFoundException("No house detail exists in the database.");
        }

        return ResponseEntity.ok(AllHouseResponse.builder()
                                                 .message("Returning all houses")
                                                 .houses(houseList)
                                                 .build());
    }
}
