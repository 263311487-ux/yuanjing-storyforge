import json,unittest,subprocess
from unittest.mock import patch
from pathlib import Path
from ai_comic_drama.seedance import SeedanceCLI
ROOT=Path(__file__).parents[1]
class Seedance(unittest.TestCase):
 def setUp(self): self.m=json.loads((ROOT/'examples/episode.json').read_text()); self.s=self.m['shots'][0]
 def test_plan_is_network_free(self):
  p=SeedanceCLI(execute=False); self.assertFalse(p.execute); self.assertTrue(p.estimate(self.m)['requires_network'])
 def test_command(self):
  c=SeedanceCLI().command(self.s); self.assertEqual(c[1],'generate'); self.assertIn('--model',c); self.assertNotIn('--wait',c)
 def test_submit_blocked_by_default(self):
  j=SeedanceCLI().submit_shot(self.s,'r1'); self.assertEqual(j.status,'blocked')
 def test_parse_task_id_shapes(self):
  self.assertEqual(SeedanceCLI.parse_task_id('{"task_id":"abc"}'),'abc')
  self.assertEqual(SeedanceCLI.parse_task_id('{"id":"xyz"}'),'xyz')
  self.assertEqual(SeedanceCLI.parse_task_id('not-json'),'')
 def test_status_mapping(self):
  self.assertEqual(SeedanceCLI.map_status({'status':'completed'}),'succeeded')
  self.assertEqual(SeedanceCLI.map_status({'state':'processing'}),'running')
  self.assertEqual(SeedanceCLI.map_status({'status':'error'}),'failed')
 def test_success_exit_without_task_id_is_failed(self):
  with patch('ai_comic_drama.seedance.subprocess.run',return_value=subprocess.CompletedProcess([],0,'{"success":true}','')):
   job=SeedanceCLI(execute=True).submit_shot(self.s,'r1')
  self.assertEqual(job.status,'unknown'); self.assertIn('missing_task_id',job.evidence['error'])
 def test_submit_timeout_is_recorded_as_failed_job(self):
  with patch('ai_comic_drama.seedance.subprocess.run',side_effect=subprocess.TimeoutExpired(['seedance'],3)) as run:
   job=SeedanceCLI(execute=True,submit_timeout=3).submit_shot(self.s,'r1')
  self.assertEqual(job.status,'unknown'); self.assertEqual(job.evidence['error'],'timeout')
  self.assertEqual(run.call_args.kwargs['timeout'],3)
 def test_poll_timeout_is_recorded_without_raising(self):
  with patch('ai_comic_drama.seedance.subprocess.run',side_effect=subprocess.TimeoutExpired(['seedance'],2)) as run:
   job=SeedanceCLI(poll_timeout=2).poll('task-1')
  self.assertEqual(job.status,'running'); self.assertEqual(job.evidence['error'],'timeout')
  self.assertEqual(run.call_args.kwargs['timeout'],2)
 def test_poll_rejects_mismatched_task_id(self):
  response=subprocess.CompletedProcess([],0,'{"task_id":"other","status":"completed"}','')
  with patch('ai_comic_drama.seedance.subprocess.run',return_value=response):
   job=SeedanceCLI().poll('task-1')
  self.assertEqual(job.status,'failed'); self.assertEqual(job.evidence['error'],'task_id_mismatch')
 def test_download_timeout_is_recorded(self):
  with patch('ai_comic_drama.seedance.subprocess.run',side_effect=subprocess.TimeoutExpired(['seedance'],2)) as run:
   job=SeedanceCLI(download_timeout=2).download('task-1',Path('/tmp/storyforge-timeout.mp4'))
  self.assertEqual(job['status'],'failed'); self.assertEqual(job['error'],'timeout')
  self.assertEqual(run.call_args.kwargs['timeout'],2)
