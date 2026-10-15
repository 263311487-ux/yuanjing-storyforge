import json, tempfile, unittest
from pathlib import Path
from ai_comic_drama.providers import MockProvider, Job
from ai_comic_drama.runner import run_manifest
ROOT=Path(__file__).parents[1]
class Runner(unittest.TestCase):
 def setUp(self): self.m=json.loads((ROOT/'examples/episode.json').read_text())
 def test_dry_run(self):
  with tempfile.TemporaryDirectory() as d: self.assertEqual(run_manifest(self.m,MockProvider(),Path(d)/'s.json',dry_run=True)['status'],'dry-run')
 def test_resume(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'s.json'; a=run_manifest(self.m,MockProvider(),p); b=run_manifest(self.m,MockProvider(),p); self.assertEqual(a['attempts'],2); self.assertEqual(b['attempts'],2); self.assertEqual(b['status'],'succeeded')
 def test_failed_shot_review(self):
  with tempfile.TemporaryDirectory() as d:
   s=run_manifest(self.m,MockProvider(['S02']),Path(d)/'s.json'); self.assertEqual(s['status'],'needs-review'); self.assertEqual(s['shots']['S02']['status'],'failed')
 def test_unknown_submission_is_not_retried(self):
  class UnknownProvider(MockProvider):
   def submit_shot(self, shot, run_id): return Job(shot['id'], 'unknown-run', 'unknown', self.name, {'error':'timeout'})
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'s.json'; s=run_manifest(self.m,UnknownProvider(),p)
   self.assertEqual(s['status'],'needs-review'); self.assertEqual(s['shots']['S01']['status'],'unknown')
   s2=run_manifest(self.m,UnknownProvider(),p); self.assertEqual(s2['attempts'],2)

 def test_failed_download_retries_same_job_without_resubmission(self):
  class DownloadProvider(MockProvider):
   def __init__(self): self.submits=0; self.downloads=0
   def submit_shot(self, shot, run_id):
    self.submits+=1; return Job(shot['id'],'paid-job','submitted',self.name,{})
   def download(self, job_id, output):
    self.downloads+=1
    return {'status':'failed' if self.downloads==1 else 'succeeded'}
  with tempfile.TemporaryDirectory() as d:
   m=dict(self.m,shots=self.m['shots'][:1]); provider=DownloadProvider(); p=Path(d)/'s.json'
   run_manifest(m,provider,p); second=run_manifest(m,provider,p)
   self.assertEqual(provider.submits,1)
   final=run_manifest(m,provider,p)
   self.assertEqual(provider.submits,1); self.assertEqual(final['status'],'succeeded')
