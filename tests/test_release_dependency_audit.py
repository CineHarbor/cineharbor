import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit',ROOT/'scripts/release-dependency-audit.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

class AuditTests(unittest.TestCase):
    def node(self):
        return {'metadata':{'vulnerabilities':{x:0 for x in ['info','low','moderate','high','critical','total']}},'advisories':{}}
    def rust(self):
        return {'vulnerabilities':{'found':False,'count':0,'list':[]},'warnings':{}}
    def test_pinned_inputs(self):
        self.assertEqual(len(audit.validate_inputs(json.loads((ROOT/'docs/releases/1.0.0/audit-inputs.json').read_text()))),6)
    def test_mutable_or_missing_inputs_fail(self):
        data={'schema_version':1,'repositories':{x:'a'*40 for x in audit.REPOSITORIES}}
        data['repositories']['cineharbor-web']='main'
        with self.assertRaises(ValueError):audit.validate_inputs(data)
        data['repositories'].pop('cineharbor-web')
        with self.assertRaises(ValueError):audit.validate_inputs(data)
    def test_only_explicit_clean_node_result_passes(self):
        self.assertTrue(audit.audit_is_clean('node',0,self.node()))
        for obj in [None,{},[],{'error':'unavailable'}, {'metadata':{'vulnerabilities':{}}}]:
            self.assertFalse(audit.audit_is_clean('node',0,obj))
    def test_node_findings_or_registry_failure_never_pass(self):
        for severity in ['info','low','moderate','high','critical']:
            obj=self.node();obj['metadata']['vulnerabilities'][severity]=1
            self.assertFalse(audit.audit_is_clean('node',0,obj))
        for code in [1,124,127,-9]: self.assertFalse(audit.audit_is_clean('node',code,self.node()))
    def test_ignored_advisory_cannot_be_hidden_by_zero_counts(self):
        obj=self.node();obj['advisories']={'GHSA-test':{'severity':'high'}}
        self.assertFalse(audit.audit_is_clean('node',0,obj))
    def test_clean_rust_result_passes(self):
        self.assertTrue(audit.audit_is_clean('rust',0,self.rust()))
    def test_rust_findings_warnings_and_bad_schema_fail(self):
        for replacement in [{'found':True,'count':1,'list':[{}]},{'found':False,'count':False,'list':[]},{'found':False,'count':0}]:
            obj=self.rust();obj['vulnerabilities']=replacement
            self.assertFalse(audit.audit_is_clean('rust',0,obj))
        obj=self.rust();obj['warnings']={'unmaintained':[{}]}
        self.assertFalse(audit.audit_is_clean('rust',0,obj))
    def test_node_boolean_or_string_counts_are_not_evidence(self):
        for invalid in [False,'0',None]:
            obj=self.node();obj['metadata']['vulnerabilities']['low']=invalid
            self.assertFalse(audit.audit_is_clean('node',0,obj))
    def test_unknown_ecosystem_fails(self):
        self.assertFalse(audit.audit_is_clean('other',0,self.rust()))
    def test_capture_preserves_failed_process_and_logs(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(audit.subprocess,'run',return_value=subprocess.CompletedProcess(['x'],1,b'{"error":"failed"}',b'stderr')):
            step,data=audit.capture(['x'],Path(tmp),Path(tmp),'audit')
            self.assertEqual(step['exit_code'],1);self.assertEqual(data,{'error':'failed'})
            self.assertEqual((Path(tmp)/'audit.stderr').read_bytes(),b'stderr')
    def test_missing_tool_is_error_not_skip(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(audit.subprocess,'run',side_effect=FileNotFoundError):
            step,data=audit.capture(['x'],Path(tmp),Path(tmp),'audit')
            self.assertEqual(step['exit_code'],127);self.assertIsNone(data)
    def test_timeout_retains_partial_evidence(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(audit.subprocess,'run',side_effect=subprocess.TimeoutExpired(['x'],1,output=b'partial')):
            step,_=audit.capture(['x'],Path(tmp),Path(tmp),'audit')
            self.assertEqual(step['exit_code'],124);self.assertEqual((Path(tmp)/'audit.stdout').read_bytes(),b'partial')

if __name__=='__main__':unittest.main()
