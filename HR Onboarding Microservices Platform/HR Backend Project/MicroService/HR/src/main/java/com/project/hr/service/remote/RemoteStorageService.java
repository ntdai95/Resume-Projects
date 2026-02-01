package com.project.hr.service.remote;

import com.project.hr.domain.response.storage.FileResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@FeignClient("storage")
public interface RemoteStorageService {

    @PostMapping("storage/file/upload")
    FileResponse uploadFile(@RequestParam(value = "file") MultipartFile file);

    @GetMapping("storage/file/download/{fileName}")
    ResponseEntity<ByteArrayResource> downloadFile(@PathVariable String fileName);


    @DeleteMapping("storage/file/delete/{fileName}")
    ResponseEntity<String> deleteFile(@PathVariable String fileName);
}
