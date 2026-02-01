package com.project.onboard.service.remote;

import com.project.onboard.domain.response.storage.FileResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@FeignClient("storage")
public interface RemoteStorageService {

    @RequestMapping(value = "storage/file/upload", method = RequestMethod.POST, consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    FileResponse uploadFile(@RequestPart(value = "file") MultipartFile file);

    @GetMapping("storage/file/download/{fileName}")
    ResponseEntity<ByteArrayResource> downloadFile(@PathVariable String fileName);


    @DeleteMapping("storage/file/delete/{fileName}")
    ResponseEntity<String> deleteFile(@PathVariable String fileName);
}
