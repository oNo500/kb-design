"""Stable readers must keep the last verified build after failed publication."""
import importlib
import json
from pathlib import Path
import unittest
import test_system_build as fixtures


class PublicationTests(unittest.TestCase):
    setUp = fixtures.SystemBuildTests.setUp
    save = fixtures.SystemBuildTests.save

    def publication(self):
        try:return importlib.import_module('kb_vocab.publication')
        except ModuleNotFoundError:self.fail('versioned publication is not implemented')

    def test_failed_build_preserves_current_and_completed_versions(self):
        api=self.publication();root=self.root/'published'
        api.build_versioned(self.path,root,'first')
        first=(root/'current').resolve()
        self.config['domains'][0]['branches'][0]['uri']='urn:missing';self.save()
        with self.assertRaises(ValueError):api.build_versioned(self.path,root,'failed')
        self.assertEqual((root/'current').resolve(),first)
        self.assertFalse((root/'versions/failed').exists())

    def test_switch_and_rollback_preserve_versions_and_reject_tampering(self):
        api=self.publication();root=self.root/'published'
        api.build_versioned(self.path,root,'first')
        self.config['domains'][0]['whole_sources']=['b'];self.save()
        api.build_versioned(self.path,root,'second')
        self.assertEqual((root/'current').resolve(),(root/'versions/second').resolve())
        api.activate_version(root,'first')
        self.assertEqual((root/'current').resolve(),(root/'versions/first').resolve())
        (root/'versions/second/vocabulary.ttl').write_text('tampered')
        with self.assertRaises(ValueError):api.activate_version(root,'second')
        self.assertEqual((root/'current').resolve(),(root/'versions/first').resolve())

    def test_non_symlink_current_and_path_escape_are_rejected(self):
        api=self.publication();root=self.root/'published';(root/'current').mkdir(parents=True)
        (root/'current/keep').write_text('user data')
        with self.assertRaises(ValueError):api.build_versioned(self.path,root,'first')
        self.assertEqual((root/'current/keep').read_text(),'user data')
        with self.assertRaises(ValueError):api.activate_version(root,'../outside')
