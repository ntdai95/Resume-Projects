package com.project.storageservice.controller;

import com.project.storageservice.domain.FileResponse;
import com.project.storageservice.service.StorageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/file")
public class StorageController {

    StorageService service;

    @Autowired
    public StorageController(StorageService service){
        this.service = service;
    }

    @PostMapping("/upload")
    public FileResponse uploadFile(@RequestParam(value = "file") MultipartFile file){
        return FileResponse.builder().Message("upload success!").Success(true).fileStatus(service.uploadFile(file)).build();
    }

    @GetMapping("/download/{fileName}")
    public ResponseEntity<ByteArrayResource> downloadFile(@PathVariable String fileName){
        byte[] data = service.downloadFile(fileName);
        ByteArrayResource resource = new ByteArrayResource(data);
        return ResponseEntity
                .ok()
                .contentLength(data.length)
                .header("Content-type", "application/octet-stream")
                .header("Content-Disposition", "attachment; fileName=\""+ fileName + "\"")
                .body(resource);
    }

    @DeleteMapping("/delete/{fileName}")
    public ResponseEntity<String> deleteFile(@PathVariable String fileName){
        return new ResponseEntity<>(service.deleteFile(fileName), HttpStatus.OK);
    }
}
