import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class Review(unittest.TestCase):
 def test_public_docs_explain_bound_file_approval_and_live_provider_limit(self):
  for name in ('README.md','README_EN.md','SKILL.md'):
   text=(ROOT/name).read_text()
   with self.subTest(name=name):
    self.assertIn('--file',text)
    self.assertIn('real paid run',text.lower())

 def test_publish_approval_binds_media_and_manifest_hashes(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); qa=root/'qa_result.json'; video=root/'master.mp4'; subs=root/'episode.srt'; manifest=root/'episode.json'
   qa.write_text(json.dumps({'status':'PASS'})); video.write_bytes(b'video'); subs.write_text('1\n00:00:00,000 --> 00:00:01,000\nhello\n'); manifest.write_text('{}')
   subprocess.run([sys.executable,str(ROOT/'scripts/approve_publish.py'),'--qa',str(qa),'--approved-by','reviewer','--basis','release review','--file',str(video),'--file',str(subs),'--file',str(manifest)],check=True)
   approval=json.loads((root/'publish_approval.json').read_text())
   self.assertEqual(approval['status'],'APPROVED')
   self.assertEqual({x['path'] for x in approval['files']},{str(video.resolve()),str(subs.resolve()),str(manifest.resolve())})

 def test_missing_approval_file_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); qa=root/'qa.json'; qa.write_text(json.dumps({'status':'PASS'}))
   p=subprocess.run([sys.executable,str(ROOT/'scripts/approve_publish.py'),'--qa',str(qa),'--approved-by','reviewer','--basis','review','--file',str(root/'missing.mp4')],capture_output=True,text=True)
   self.assertNotEqual(p.returncode,0); self.assertIn('approval file missing',p.stderr)

 def test_record_pending(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'qa.json'; subprocess.run([sys.executable,str(ROOT/'scripts/record_content_review.py'),'--out',str(p),'--status','PENDING_HUMAN_REVIEW','--reviewer','reviewer','--basis','not reviewed'],check=True); x=json.loads(p.read_text()); self.assertFalse(x['publish_approval'])
 def test_record_pass(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'qa.json'; subprocess.run([sys.executable,str(ROOT/'scripts/record_content_review.py'),'--out',str(p),'--status','PASS','--reviewer','reviewer','--basis','shot review','--shot','S01'],check=True); self.assertEqual(json.loads(p.read_text())['shots'][0]['status'],'REVIEWED')
 def test_recorded_pass_starts_without_publish_approval(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'qa_result.json'; subprocess.run([sys.executable,str(ROOT/'scripts/record_content_review.py'),'--out',str(p),'--status','PASS','--reviewer','reviewer','--basis','shot review'],check=True)
   self.assertFalse(json.loads(p.read_text())['publish_approval'])
