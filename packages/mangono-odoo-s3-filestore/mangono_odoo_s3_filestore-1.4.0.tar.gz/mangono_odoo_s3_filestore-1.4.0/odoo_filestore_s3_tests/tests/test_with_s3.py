import base64
import contextlib
import logging
import typing
import unittest
from unittest import mock, skipUnless

import minio

import odoo
from odoo.tests import TransactionCase

from odoo.addons.odoo_filestore_s3 import can_be_activate
from odoo.addons.odoo_filestore_s3.adapter import IrAttachementAdapter
from odoo.addons.odoo_filestore_s3.odoo_s3_fs import S3Odoo

odoo_version = odoo.release.version_info[0]
_logger = logging.getLogger(__name__)


@contextlib.contextmanager
def wrap_minio_execute() -> typing.Generator[unittest.mock.MagicMock, None, None]:
    """Wrap the named member on an object with a mock object.

    wrap_object() can be used as a context manager. Inside the
    body of the with statement, the attribute of the target is
    wrapped with a :class:`unittest.mock.MagicMock` object. When
    the with statement exits the patch is undone.

    The instance argument 'self' of the wrapped attribute is
    intentionally not logged in the MagicMock call. Therefore
    wrap_object() can be used to check all calls to the object,
    but not differentiate between different instances.
    """
    mock = unittest.mock.MagicMock()
    real_attribute = minio.Minio._execute

    def mocked_attribute(self, *args, **kwargs):
        kwargs_light = dict(kwargs)
        kwargs_light.pop("headers", None)
        kwargs_light.pop("preload_content", None)
        kwargs_light.pop("no_body_trace", None)
        kwargs_light.pop("query_params", None)
        _logger.info("call _execute %s %s", args, kwargs_light)
        mock.__call__(*args, **kwargs_light)
        return real_attribute(self, *args, **kwargs)

    with unittest.mock.patch.object(minio.Minio, "_execute", mocked_attribute):
        yield mock


@skipUnless(can_be_activate(odoo_version), f"Odoo {odoo_version} version not supported")
class OdooFilestoreS3TestPatcher(TransactionCase):
    def setUp(self):
        super().setUp()
        self.attachmentModel = self.env["ir.attachment"]
        self.s3 = S3Odoo.from_env(self.env.cr.dbname)
        self.adapter = IrAttachementAdapter(odoo_version)

    # region: Helper method

    def invalidate(self, obj):
        if odoo_version < 16:
            obj.invalidate_cache(ids=obj.ids)
        else:
            obj.invalidate_recordset()

    # endregion

    # region : Tests methods
    def test_01_params(self):
        self.assertTrue(
            "odoo_filestore_s3" in odoo.conf.server_wide_modules,
            "'odoo_filestore_s3' should be in load to run this tests",
        )

    def test_create_attachment(self):
        """
        Test file write, and check de file is in the local storage and in the s3 storage
        """
        value = b"binary test_create_attachment55"
        with wrap_minio_execute() as minio_execute_put:
            att = self.env["ir.attachment"].create(
                {
                    "name": "test_file",
                    "datas": base64.b64encode(value),
                }
            )
            # One call for the real file
            # One call for the garbage collect pointer
            minio_execute_put.assert_has_calls(
                [
                    mock.call("PUT", self.s3.bucket.name, att.store_fname, body=value),
                    mock.call("PUT", self.s3.bucket.name, "checklist/" + att.store_fname, body=b""),
                ],
                any_order=True,
            )

    def test_read_optimized(self):
        """
        Test file write, and check de file is in the local storage and in the s3 storage
        """
        value = b"binary test_read_optimized"
        att = self.env["ir.attachment"].create(
            {
                "name": "test_file",
                "datas": base64.b64encode(value),
            }
        )
        self.invalidate(att)
        self.assertTrue(
            self.s3.file_exist(att.store_fname),
            "The file should exit on the remote S3. Ensure using direct s3 connection",
        )
        IrAttachementAdapter.remove_from_cache(att)
        with wrap_minio_execute() as minio_execute_put:
            minio_execute_put.assert_not_called()
            # force trigger to not use Odoo cache
            self.assertEqual(att._file_read(att.store_fname), self.adapter.encode_content(value))
            # Assert only 1 call to s3 is executed
            minio_execute_put.assert_called_once_with("GET", self.s3.bucket.name, att.store_fname)
            self.assertTrue(IrAttachementAdapter.exist_in_cache(att), "The file exit on local disc filestore")
            minio_execute_put.reset_mock()
            # Trigger an another _file_read, but with cache
            self.assertEqual(att._file_read(att.store_fname), self.adapter.encode_content(value))
            # No S3 call is executed
            minio_execute_put.assert_not_called()

            # 2. Retry a second call to be sure the cache is not corrupt
            # Remove cache
            IrAttachementAdapter.remove_from_cache(att)
            # Force read file, s3 should be called
            self.assertEqual(att._file_read(att.store_fname), self.adapter.encode_content(value))
            # Assert S3 is called
            minio_execute_put.assert_called_once_with("GET", self.s3.bucket.name, att.store_fname)

    def test_read_and_store_in_cache(self):
        """
        Test file write, and check de file is in the local storage and in the s3 storage
        """
        value = b"binary test_read_and_store_in_cache"
        att = self.env["ir.attachment"].create(
            {
                "name": "test_file",
                "datas": base64.b64encode(value),
            }
        )
        self.assertTrue(self.s3.file_exist(att.store_fname))
        self.assertTrue(IrAttachementAdapter.exist_in_cache(att))
        IrAttachementAdapter.remove_from_cache(att)
        self.assertFalse(IrAttachementAdapter.exist_in_cache(att))
        self.invalidate(att)
        self.assertEqual(att.datas, base64.b64encode(value))  # This trigger a Odoo read wich trigger _file_read on S3
        self.assertTrue(IrAttachementAdapter.exist_in_cache(att), "After the read, the file is in cache")
