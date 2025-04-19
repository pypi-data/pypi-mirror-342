import os
from unittest import mock, skipUnless
from unittest.mock import MagicMock

from odoo import release
from odoo.tests import TransactionCase

from odoo.addons.odoo_filestore_s3 import can_be_activate
from odoo.addons.odoo_filestore_s3.adapter import IrAttachementAdapter
from odoo.addons.odoo_filestore_s3.odoo_s3_fs import S3Odoo

odoo_version = release.version_info[0]


@skipUnless(odoo_version >= 16 and can_be_activate(odoo_version), "Odoo version not supported")
class OdooPatch16_17(TransactionCase):
    def setUp(self):
        super().setUp()
        self.attachmentModel = self.env["ir.attachment"]
        self.s3 = S3Odoo.from_env(self.env.cr.dbname)

    @skipUnless(odoo_version >= 18, "See test_stream_attachment_less_18")
    def test_stream_attachment_more_eq_18(self):
        attachment, mock_request = self._prepare_test()
        with mock.patch("odoo.http.request", mock_request), mock.patch(
            "odoo.addons.base.models.ir_attachment.request", mock_request
        ):
            self.execute_test(attachment)

    @skipUnless(odoo_version < 18, "See test_stream_attachment_more_eq_18")
    def test_stream_attachment_less_18(self):
        attachment, mock_request = self._prepare_test()
        with mock.patch("odoo.http.request", mock_request):
            self.execute_test(attachment)

    def execute_test(self, attachment):
        self.assertFalse(IrAttachementAdapter.exist_in_cache(attachment), "The file don't exit on cache, but on s3")
        self.env["ir.binary"]._record_to_stream(attachment, "raw")
        self.assertTrue(IrAttachementAdapter.exist_in_cache(attachment), "After _record_to_stream the file exist again")

    def _prepare_test(self):
        value = b"binary test_read_optimized"
        attachment = self.env["ir.attachment"].create(
            {
                "name": "test_file",
                "raw": value,
            }
        )
        full_path = self.attachmentModel._full_path(attachment.store_fname)
        self.assertTrue(os.path.exists(full_path), "Exist on local disk")
        IrAttachementAdapter.remove_from_cache(attachment)
        attachment.invalidate_recordset()
        mock_request = MagicMock()
        mock_request.db = self.env.cr.dbname
        return attachment, mock_request
