import logging
import os
import time
from typing import IO, Optional
from datetime import timedelta
from pathlib import Path
from minio import Minio
from minio.error import S3Error
from minio.helpers import ObjectWriteResult
from minio.commonconfig import Tags


class MinioS3:
    """Provides functionality for interacting with Minio S3"""

    def __init__(
        self,
        domain: str,
        access_key: str,
        secret_key: str,
        is_secure: bool,
    ):

        # Instantiate Minio client instance
        self.client = Minio(domain, access_key=access_key, secret_key=secret_key, secure=is_secure)

    @staticmethod
    def _validate_str_dict_(tag_dict: dict) -> None:
        """
        Validate that the keys and values of the tag_dict are of type str.
        :param tag_dict: A dictionary of tags
        :return: None
        """
        assert isinstance(tag_dict, dict), "tag_dict is not of type dict"
        for k, v in tag_dict.items():
            assert isinstance(k, str), f'tag_dict key "{k}" is not of type str'
            assert isinstance(v, str), f'tag_dict value "{v}" (key "{k}") is not of type str'
            # trailing or leading space characters are trimmed off by the minio lib,
            # and cause SignatureDoesNotMatch error
            if k != k.strip():
                assert k.strip() not in tag_dict, (
                    f'tag_dict key "{k}" contains a leading or trailing space character'
                    f" The spacing character(s) cannot be trimmed, the trimmed key"
                    f" already exist)"
                )
            assert (
                k == k.strip()
            ), f'tag_dict key "{k}" contains a leading or trailing space character'
            assert (
                v == v.strip()
            ), f'tag_dict value "{k}" contains a leading or trailing space character'

    @staticmethod
    def _convert_to_tags(tag_dict: dict) -> Tags:
        """
        Convert a dictionary of tags to a Tags object.
        :param tag_dict: A dictionary of tags
        :return: A Tags object
        """
        assert tag_dict, "Invalid tag_dict, it must be non-empty dict"
        MinioS3._validate_str_dict_(tag_dict)
        new_tag_dict = Tags(for_object=True)
        new_tag_dict.update(tag_dict)
        return new_tag_dict

    def list_objects(self, bucket_name: str, prefix: str, recursive: bool) -> iter:
        """
        List objects and their metadata and tags. Filter using prefix.
        :param bucket_name: The name of the bucket
        :param prefix: The prefix to filter objects
        :param recursive: If True, list objects recursively
        :return: An iterator of objects
        """
        logging.info(f'Listing objects from bucket "{bucket_name}" (using prefix "{prefix}")...')
        gen_objects = self.client.list_objects(
            bucket_name, prefix=prefix, recursive=recursive, include_user_meta=True
        )
        logging.info("Success")
        return gen_objects

    def get_object(self, bucket_name: str, object_name: str) -> bytes:
        """
        Get object_name from bucket bucket_name. Return the data (HTTPResponse.data bytes).
        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :return: The data of the object
        """
        logging.info(f'Getting "{object_name}" from bucket "{bucket_name}"...')
        response = self.client.get_object(bucket_name, object_name)
        return response.data

    def download_file(
        self, bucket_name: str, object_name: str, output_file: Path, overwrite: bool = True
    ) -> bool:
        """
        Fetch object_name and write it to output_file. Return True if the file was downloaded,
        False otherwise.
        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :param output_file: The path to the output file
        :param overwrite: If True, overwrite the file if it already exists
        :return: True if the file was downloaded, False otherwise
        """
        if not overwrite and os.path.isfile(output_file):
            logging.info(f'Target file "{output_file}" already exist. Not downloaded')
            return False
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "wb") as fw:
            fw.write(self.get_object(bucket_name, object_name))
        logging.info(
            f'File "{object_name}" ("{output_file}") has been successfully'
            f' downloaded from bucket "{bucket_name}"'
        )
        return True

    def download_files(
        self,
        bucket_name: str,
        prefix: str,
        output_dir: Path,
        overwrite: bool = False,
        ignore_contains: list = None,
    ) -> int:
        """
        Fetch object_name and write it to output_file.
        Return True if the file was downloaded, False otherwise.
        :param bucket_name: The name of the bucket
        :param prefix: The prefix to filter objects
        :param output_dir: The path to the output directory
        :param overwrite: If True, overwrite the file if it already exists
        :param ignore_contains: List of strings to ignore in the object name
        :return: The number of files downloaded
        """
        count = 0
        for obj in self.client.list_objects(bucket_name, prefix=prefix, recursive=True):
            if obj.object_name.endswith("/"):
                # never reached?
                # folder-like cannot be "get"
                continue

            obj_name = os.path.relpath(obj.object_name, prefix)
            if ignore_contains:
                if [p for p in ignore_contains if p in obj.object_name]:
                    continue

            success = self.download_file(
                bucket_name,
                obj.object_name,
                Path(os.path.join(output_dir, obj_name)),
                overwrite=overwrite,
            )
            if success:
                count += 1
        logging.info(
            f'{count} file(s) with "{prefix}" have been successfully'
            f' downloaded from bucket "{bucket_name}"'
        )
        return count

    def put_object(
        self,
        bucket_name: str,
        object_name: str,
        data: IO,
        content_type: str = "application/octet-stream",  # default value if set to None
        length: int = -1,
        metadata_dict: dict = None,
        tag_dict: dict = None,
        multipart_threshold: int = 0,
        skip_exist: bool = True,
    ) -> Optional[ObjectWriteResult]:
        """
        Put an object in bucket. Set skip_exist to True to avoid
        copying the object if already in the bucket.
        Return ObjectWriteResult if save else return None
        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :param data: The data to write
        :param content_type: The content type of the object
        :param length: The length of the object
        :param metadata_dict: The metadata of the object
        :param tag_dict: The tags of the object
        :param multipart_threshold: The threshold to use multipart upload
        :param skip_exist: If True, skip copying the object if it already exists
        :return: ObjectWriteResult if save else None
        """
        if skip_exist and self.object_exist(bucket_name, object_name):
            logging.info(
                f'Skip putting "{object_name}" to bucket "{bucket_name}", object already exists'
            )
            return

        if metadata_dict:
            MinioS3._validate_str_dict_(metadata_dict)
        if tag_dict:
            tag_dict = MinioS3._convert_to_tags(tag_dict)

        logging.info(f'Putting "{object_name}" to bucket "{bucket_name}"...')

        if length != -1 and length > multipart_threshold:
            length = -1

        for i in range(3):
            try:
                result = self.client.put_object(
                    bucket_name,
                    object_name,
                    data,
                    length,
                    content_type=content_type,
                    metadata=metadata_dict,
                    tags=tag_dict,
                    part_size=0 if length != -1 else 10 * 1024 * 1024,
                )
                break
            except S3Error as e:
                logging.info(f'Fail with error: "{e}"')
                if "SignatureDoesNotMatch" in str(e):
                    if self.object_exist(bucket_name, object_name):
                        logging.info("Object found on the bucket, trying to delete..")
                        self.delete_object(
                            bucket_name, object_name
                        )  # should capture eventual exception?
                        logging.info("Object deleted..")
                    if i == 2:
                        raise e
                    logging.info(f"Retrying in 10 second ({i + 1})")
                    time.sleep(10)
                else:
                    raise e
        logging.info("Success")
        return result

    def put_objects(
        self,
        bucket_name: str,
        file_list: list,
        multipart_threshold: int = 0,
        skip_exist: bool = True,
    ) -> list[Optional[ObjectWriteResult]]:
        """
        Put a list of files as objects in storage.

        Set skip_exist to True to avoid copying object_name already in the bucket.
        The list of files must have the following structure:
        [
          [
            file_path: Path or str
            obj_name: destination on the bucket
            content_type: if None is set to 'application/octet-stream'
            length: number of bytes to write
            metadata_dict: metadata to include with the object
            tag_dict: tags to add to the object
          ]
        ]
        Return the list of ObjectWriteResult added to the bucket.
        :param bucket_name: The name of the bucket
        :param file_list: The list of files to put
        :param multipart_threshold: The threshold to use multipart upload
        :param skip_exist: If True, skip copying the object if it already exists
        :return: The list of ObjectWriteResult added to the bucket
        """
        saved_files = []
        assert isinstance(file_list, list), "Invalid file_list, it is not a list"
        for file_path, obj_name, content_type, length, metadata_dict, tag_dict in file_list:
            result = self.put_object(
                bucket_name,
                obj_name,
                open(file_path, "rb"),
                content_type=content_type,
                length=length,
                metadata_dict=metadata_dict,
                tag_dict=tag_dict,
                multipart_threshold=multipart_threshold,
                skip_exist=skip_exist,
            )
            if result:
                saved_files.append(result)
        logging.info(f'{len(saved_files)} file(s) uploaded to bucket "{bucket_name}"')
        return saved_files

    def put_folder(
        self, bucket_name: str, source_folder: str, destination: str, skip_exist: bool = False
    ) -> list[Optional[ObjectWriteResult]]:
        """
        Put all folders/files from the source_folder in bucket destination (prefix).
        The source_folder itself is not copy to the bucket, its name won't be part
        of the object names

        Set skip_exist to True to avoid copying object_name already in the bucket.
        Return the list of ObjectWriteResult added to the bucket.
        :param bucket_name: The name of the bucket
        :param source_folder: The source folder to copy
        :param destination: The destination on the bucket
        :param skip_exist: If True, skip copying the object if it already exists
        :return: The list of ObjectWriteResult added to the bucket
        """
        assert os.path.isdir(source_folder), (
            f'cannot send objects to bucket, source_folder "{source_folder}"' f" is not a directory"
        )
        assert len(os.listdir(source_folder)) != 0, (
            f'cannot send objects to bucket, source_folder "{source_folder}"' f" is empty"
        )
        assert destination.endswith("/"), 'Destination must end with "/"'
        files_to_send = []
        for root, folders, files in os.walk(source_folder):
            for name in files:
                file_path = os.path.join(root, name)
                rel_path = os.path.relpath(file_path, source_folder)
                files_to_send.append(
                    [file_path, os.path.join(destination, rel_path), None, -1, None, None]
                )

        return self.put_objects(bucket_name, files_to_send, skip_exist=skip_exist)

    def delete_object(self, bucket_name: str, object_name: str) -> None:
        """
        Delete object_name from bucket_name.
        :param bucket_name: The name of the bucket to delete from
        :param object_name: The name of the object to delete
        :return:
        """
        logging.info(f'Removing "{object_name}" from bucket "{bucket_name}"...')
        self.client.remove_object(bucket_name, object_name)
        logging.info("Success")

    def stat_object(self, bucket_name: str, object_name: str) -> object:
        """
        Return Object(
            bucket_name,
            object_name,
            last_modified=last_modified,
            etag=response.headers.get("etag", "").replace('"', ""),
            size=int(response.headers.get("content-length", "0")),
            content_type=response.headers.get("content-type"),
            metadata=custom_metadata,
            version_id=response.headers.get("x-amz-version-id"),
        ).
        """
        logging.info(f'Stat object "{bucket_name}" from bucket "{object_name}"...')
        obj = self.client.stat_object(bucket_name, object_name)
        logging.info("Success")
        return obj

    def get_object_tags(self, bucket_name: str, object_name: str) -> dict:
        """
        Get tags for object_name in bucket_name.
        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :return: A dictionary of tags
        """
        return self.client.get_object_tags(bucket_name, object_name)

    def set_object_tags(self, bucket_name: str, object_name: str, tag_dict: dict[str, str]) -> None:
        """
        Set tags (tag_dict) to existing object_name in bucket_name.
        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :param tag_dict: The dictionary of tags to set
        :return: None
        """
        tags = self._convert_to_tags(tag_dict)
        self.client.set_object_tags(bucket_name, object_name, tags)

    def delete_object_tags(self, bucket_name: str, object_name: str) -> None:
        """
        Delete the tags assigned to the object_name in bucket_name.
        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :return: None
        """
        self.client.delete_object_tags(bucket_name, object_name)

    def object_exist(self, bucket_name: str, object_name: str) -> bool:
        """
        Return True if object_name is in bucket bucket_name, False otherwise.
        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :return: True if object_name is in bucket bucket_name, False otherwise
        """
        try:
            self.get_object_tags(bucket_name, object_name)
        except S3Error as exc:
            if exc.code == "NoSuchTagSet":
                return True
            elif exc.code == "NoSuchKey":
                return False
            raise exc
        return True

    def get_presigned_url(
        self, bucket_name: str, object_name: str, expires: timedelta = timedelta(days=7)
    ) -> str:
        """
        Get presigned URL of an object to download its data with expiry time.
        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :param expires: The expiry time of the URL
        :return: The presigned URL
        """
        return self.client.get_presigned_url(
            "GET",
            bucket_name,
            object_name,
            expires=expires,
        )
