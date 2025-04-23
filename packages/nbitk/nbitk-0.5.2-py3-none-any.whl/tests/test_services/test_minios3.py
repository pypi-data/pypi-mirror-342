import os
import io
import shutil
from pathlib import Path
import pytest
import requests
from nbitk.Services.MinioS3 import MinioS3
from testcontainers.minio import MinioContainer


class TestClass:
    @pytest.fixture()
    def minioc(self):
        with MinioContainer() as minioc:
            client = minioc.get_client()
            client.make_bucket("test-bucket")
            test_content = b"test_content"
            for f in ["testfile1.txt", "testfile2.txt", "test_folder/testfile3.txt", "test_folder/testfile4.txt"]:
                client.put_object(
                    "test-bucket",
                    f,
                    io.BytesIO(test_content),
                    length=len(test_content),
                )

            yield minioc

    @pytest.fixture()
    def client(self, minioc):
        return minioc.get_client()

    @pytest.fixture()
    def minio_conn(self, minioc):
        conf = minioc.get_config()
        return MinioS3(
            conf['endpoint'],
            conf['access_key'],
            conf['secret_key'],
            False,  # is_secure
        )

    def test_list_objects(self, minio_conn):
        res = [obj for obj in minio_conn.list_objects(
            'test-bucket',
            '',
            False  # recursive off
        )]
        assert sorted([e.object_name for e in res]) == ['test_folder/', 'testfile1.txt', 'testfile2.txt']

    def test_list_objects_recur(self, minio_conn):
        res = [obj for obj in minio_conn.list_objects(
            'test-bucket',
            '',
            True  # recursive on
        )]
        assert sorted([e.object_name for e in res]) == ['test_folder/testfile3.txt',
                                                        'test_folder/testfile4.txt',
                                                        'testfile1.txt',
                                                        'testfile2.txt']

    def test_list_objects_prefix(self, minio_conn):
        res = [obj for obj in minio_conn.list_objects(
            'test-bucket',
            'test_folder/',
            False  # recursive off
        )]
        assert sorted([e.object_name for e in res]) == ['test_folder/testfile3.txt',
                                                        'test_folder/testfile4.txt']

    def test_get_object_content(self, minio_conn):
        data = minio_conn.get_object(
            'test-bucket',
            'test_folder/testfile3.txt',
        )
        assert data == b'test_content'

    def test_download_file(self, tmp_path, minio_conn):
        output_file = Path(f'{tmp_path}/local_testfile3.test')
        success = minio_conn.download_file(
            'test-bucket',
            'test_folder/testfile3.txt',
            output_file
        )

        with open(output_file) as fh:
            assert fh.readlines() == ['test_content']
        assert success

        output_file = Path(f'{tmp_path}/local_testfile3.test')
        success = minio_conn.download_file(
            'test-bucket',
            'test_folder/testfile3.txt',
            output_file,
            overwrite=False
        )
        assert not success

    @pytest.mark.parametrize(
        "prefix, ignore_list, count, folder_files", [
            ("", [], 4, ['testfile1.txt', 'testfile2.txt', 'testfile3.txt', 'testfile4.txt']),
            ("test_folder/", [], 2, ['testfile3.txt', 'testfile4.txt']),
            ("not_exist", [], 0, []),
            ("", ['test_folder'], 2, ['testfile1.txt', 'testfile2.txt']),
            ("", ['not_exist'], 4, ['testfile1.txt', 'testfile2.txt', 'testfile3.txt', 'testfile4.txt']),
            ("", ['testfile'], 0, []),
        ])
    def test_download_files(self, tmp_path, minio_conn, prefix, ignore_list, count, folder_files):
        output_folder = Path(f'{tmp_path}/local_test_dir')
        df_count = minio_conn.download_files(
            'test-bucket',
            prefix,
            output_folder,
            overwrite=False,
            ignore_contains=ignore_list
        )
        assert df_count == count
        if folder_files:
            dfiles = []
            for _,_, files in os.walk(output_folder):
                dfiles += files
            assert sorted(dfiles) == folder_files
            # test the content of the first file
            with open(os.path.join(output_folder, dfiles[0])) as fh:
                assert fh.readlines() == ['test_content']

    def test_download_files_overwrite(self, tmp_path, minio_conn):
        output_folder = Path(f'{tmp_path}/local_test_dir')
        df_count = minio_conn.download_files(
            'test-bucket',
            'test_folder/',
            output_folder,
        )
        assert df_count == 2

        df_count = minio_conn.download_files(
            'test-bucket',
            'test_folder/',
            output_folder,
            overwrite=False
        )
        assert df_count == 0

    def test_delete_object(self, minio_conn):
        # This test depends on a method tested test_list_objects
        minio_conn.delete_object(
            'test-bucket',
            'test_folder/testfile4.txt',
        )
        assert [o.object_name for o in minio_conn.list_objects(
            'test-bucket',
            "",
            recursive=True
        )] == ['test_folder/testfile3.txt', 'testfile1.txt', 'testfile2.txt']

    def test_stat_object(self, minio_conn):
        stats = minio_conn.stat_object(
            'test-bucket',
            'test_folder/testfile4.txt',
        )
        assert stats.object_name == 'test_folder/testfile4.txt'

    def test_object_tags(self, minio_conn):
        tags = {'key': 'value'}
        minio_conn.set_object_tags(
            'test-bucket',
            'testfile1.txt', tags
        )

        fetched_tags = minio_conn.get_object_tags(
            'test-bucket',
            'testfile1.txt'
        )
        assert fetched_tags == tags
        # note that stat.tags is still None!?

        minio_conn.delete_object_tags(
            'test-bucket',
            'testfile1.txt'
        )

        fetched_tags = minio_conn.get_object_tags(
            'test-bucket',
            'testfile1.txt'
        )
        assert fetched_tags is None

    def test_object_exist(self, minio_conn):
        assert minio_conn.object_exist('test-bucket', 'testfile1.txt') is True
        assert minio_conn.object_exist('test-bucket', 'not_exist.txt') is False

    def test_get_presigned_url(self, tmp_path, minio_conn):
        url = minio_conn.get_presigned_url(
            'test-bucket',
            'testfile1.txt'
        )
        r = requests.get(url)
        dest_file = os.path.join(tmp_path, 'local_testfile1.txt')
        with open(dest_file, 'wb') as f:
            f.write(r.content)
        with open(dest_file) as fh:
            assert fh.readlines() == ['test_content']

    def test_put_object(self, minio_conn):
        # This test depends on methods tested test_stat_object and test_object_tags
        object_to_put = 'test_folder/testfile5.txt'
        tag_dict = {'tag_key1': 'tag_value1', 'tag_key2': 'tag_value2'}
        result = minio_conn.put_object(
            'test-bucket',
            object_to_put,
            io.BytesIO(b'test_put_object'),
            metadata_dict={'meta_key': "meta_value"},
            tag_dict=tag_dict,
        )
        assert result is not None and result.object_name == object_to_put

        stat = minio_conn.stat_object(
            'test-bucket',
            object_to_put
        )

        assert stat.object_name == object_to_put
        assert stat.metadata['x-amz-meta-meta_key'] == 'meta_value'
        assert stat.metadata['x-amz-tagging-count'] == '2'
        # stat.tags is None!

        fetched_tags = minio_conn.get_object_tags(
            'test-bucket',
            object_to_put
        )
        assert fetched_tags == tag_dict

        # try to put the same object
        result = minio_conn.put_object(
            'test-bucket',
            object_to_put,
            io.BytesIO(b'test_put_object')
            # skip_exist is True by default
        )
        assert result is None

        # try to put the same object one more time
        result = minio_conn.put_object(
            'test-bucket',
            object_to_put,
            io.BytesIO(b'test_put_object'),
            skip_exist=False
        )
        assert result is not None

    def test_put_objects(self, tmp_path, minio_conn):
        # This test depends on methods tested test_stat_object and test_object_tags
        files_to_send = []
        for i in range(1, 4):
            f_name = f'test_put_file{i}.txt'
            input_file = os.path.join(tmp_path, f_name)
            with open(os.path.join(tmp_path, f_name), 'w') as fw:
                fw.write(str(i))

            files_to_send.append(
                [
                    input_file,  # source
                    f'new_folder/{f_name}',  # dest
                    None,  # content_type
                    -1,  # length
                    {f'meta_key{i}': f'meta_value{i}'},
                    {f'tag_key{i}-1': f'tag_value{i}-1', f'tag_key{i}-2': f'tag_value{i}-2'}
                ]
            )

        save_result = minio_conn.put_objects(
            'test-bucket',
            files_to_send[:2],
        )
        assert isinstance(save_result, list) and len(save_result) == 2

        objects = minio_conn.list_objects(
            'test-bucket',
            'new_folder',
            True
        )
        assert sorted([o.object_name for o in objects]) == [
            'new_folder/test_put_file1.txt',
            'new_folder/test_put_file2.txt'
        ]

        stat = minio_conn.stat_object(
            'test-bucket',
            'new_folder/test_put_file2.txt'
        )

        assert stat.object_name == 'new_folder/test_put_file2.txt'
        assert stat.metadata['x-amz-meta-meta_key2'] == 'meta_value2'
        assert stat.metadata['x-amz-tagging-count'] == '2'
        # stat.tags is None!

        fetched_tags = minio_conn.get_object_tags(
            'test-bucket',
            'new_folder/test_put_file2.txt'
        )
        assert fetched_tags == {'tag_key2-1': 'tag_value2-1', 'tag_key2-2': 'tag_value2-2'}

        save_result = minio_conn.put_objects(
            'test-bucket',
            files_to_send[1:],
            skip_exist=True
        )
        assert isinstance(save_result, list) and len(save_result) == 1
        assert save_result[0].object_name == 'new_folder/test_put_file3.txt'

    def test_put_folder(self, tmp_path, minio_conn):
        # This test depends on methods tested in test_stat_object and test_get_object
        test_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'minio_test_folder')
        copied_test_data_folder = shutil.copytree(test_data_path, os.path.join(tmp_path, 'minio_test_folder'))

        save_result = minio_conn.put_folder(
            'test-bucket',
            copied_test_data_folder,
            'DEST/',
            skip_exist=False
        )

        objects = minio_conn.list_objects(
            'test-bucket',
            'DEST/',
            True
        )
        assert sorted([o.object_name for o in objects]) == [
            'DEST/sub_folder/sub_sub_folder/test_put_file4.txt',
            'DEST/sub_folder/test_put_file3.txt',
            'DEST/test_put_file1.txt',
            'DEST/test_put_file2.txt'
        ]

        # check the content of one file
        data = minio_conn.get_object(
            'test-bucket',
            'DEST/sub_folder/sub_sub_folder/test_put_file4.txt'
        )
        assert data == b'content4'

        # add a file to the input folder and resend it with skip_exist = True
        with open(os.path.join(copied_test_data_folder, 'sub_folder', 'test_put_file5.txt'), 'w') as fw:
            fw.write('content5')

        save_result = minio_conn.put_folder(
            'test-bucket',
            copied_test_data_folder,
            'DEST/',
            skip_exist=True
        )
        assert len(save_result) == 1
        assert save_result[0].object_name == 'DEST/sub_folder/test_put_file5.txt'