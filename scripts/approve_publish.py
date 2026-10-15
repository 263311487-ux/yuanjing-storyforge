#!/usr/bin/env python3
"""Record an explicit, auditable human publish approval in a QA report."""
import argparse,json,time,hashlib
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--qa',required=True); p.add_argument('--approved-by',required=True); p.add_argument('--basis',required=True); p.add_argument('--file',action='append',default=[],help='media, subtitle, manifest or cover file to bind to this approval'); a=p.parse_args()
path=Path(a.qa); data=json.loads(path.read_text(encoding='utf-8'))
if data.get('status')!='PASS': raise SystemExit('content QA must be PASS before approval')
if not a.approved_by.strip() or not a.basis.strip(): raise SystemExit('reviewer and basis must be nonempty')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()
files=[]
for raw in a.file:
    f=Path(raw).resolve()
    if not f.is_file(): raise SystemExit(f'approval file missing: {f}')
    files.append({'path':str(f),'sha256':sha(f)})
approval={'qa_sha256':sha(path),'status':'APPROVED','approved_by':a.approved_by,'approved_at':int(time.time()),'basis':a.basis,'content_qa':str(path.resolve()),'files':files}
out=path.parent/'publish_approval.json'; out.write_text(json.dumps(approval,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(out)
