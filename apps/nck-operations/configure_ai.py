"""Local interactive configuration; never prints credentials."""
import getpass,json,os,re
from pathlib import Path
path=Path(__file__).resolve().parent/'.ai-config.json'
print('Hubungkan Asisten NCK. API key hanya disimpan di file lokal privat.')
provider=input('Penyedia [openai / gemini]: ').strip().lower()
if provider not in ['openai','gemini']:raise SystemExit('Pilih openai atau gemini.')
model=input('ID model dari akun API penyedia: ').strip()
if not re.fullmatch(r'[A-Za-z0-9._-]+',model):raise SystemExit('ID model tidak valid.')
key=getpass.getpass('API key (tidak terlihat saat diketik): ').strip()
if not key:raise SystemExit('API key kosong; konfigurasi tidak diubah.')
config=json.loads(path.read_text()) if path.exists() else {}
config[provider]={'api_key':key,'model':model}
fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
with os.fdopen(fd,'w') as f:json.dump(config,f)
path.chmod(0o600)
print('Tersimpan. Buka kembali panel Asisten NCK; tidak perlu restart server.')
