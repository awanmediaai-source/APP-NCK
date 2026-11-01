import hashlib, json
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone
from .models import *

class RuleError(Exception): pass
FINANCE = {'admin','finance','management'}
PERMISSIONS = {
 'create_order':{'admin'}, 'allocate':{'admin','warehouse'}, 'pick':{'admin','warehouse'},
 'production':{'admin','operator'}, 'rework':{'admin','operator','qc'}, 'transfer':{'admin','operator'},
 'receive':{'admin','operator','warehouse','qc'}, 'pack':{'admin','qc'}, 'ship':{'admin','qc'},
 'cancel':{'admin'}, 'priority':{'admin'}, 'block':{'admin','operator'}, 'restock':{'admin','warehouse'},
 'approve':{'admin'}, 'reject':{'admin'}, 'design':{'admin'}, 'qc':{'admin','qc'},
}
def role(user): return user.profile.role

def integer(data,key, minimum=0):
    try:
        raw = str(data.get(key,''))
        if not raw.isdigit(): raise ValueError()
        n=int(raw)
        if n<minimum or n>100000: raise ValueError()
        return n
    except (ValueError,TypeError): raise RuleError(f'{key}: isi jumlah bulat {minimum}–100.000.')

def reason(d):
    value=str(d.get('reason','')).strip()
    if not value or len(value)>250: raise RuleError('Alasan / bukti wajib diisi (maksimal 250 karakter).')
    return value

def version(obj,d):
    if integer(d,'version') != obj.version: raise RuleError('Data berubah. Muat ulang lalu tinjau versi terbaru.')

def next_stage(job):
    route=['printing','press'] + (['cutting','vendor'] if job.sku.category=='Jersey' else []) + ['qc']
    if job.stage=='picking': return 'qc'
    return route[route.index(job.stage)+1] if job.stage in route and job.stage!='qc' else None

def job_active(job):
    if job.item and (job.item.order.cancelled or job.item.order.shipped_at):
        raise RuleError('Order ditutup. WIP dipertahankan; perlu penanganan PPIC sebelum dilanjutkan.')

def allocate_all():
    # shortcut: satu lock global menyerialkan command pilot; pecah per SKU setelah benchmark multi-user.
    orders=Order.objects.filter(cancelled=False,shipped_at=None).order_by('-priority','received_at','id')
    allocated=0
    for o in orders:
        if o.blocker: continue
        for item in o.items.select_related('sku'):
            committed=sum(r.qty for r in Reservation.objects.filter(item=item,released=False))
            # Root production jobs only; downstream work cannot create a second demand.
            production=Job.objects.filter(item=item,stage='printing').aggregate(n=Sum('incoming'))['n'] or 0
            remaining=max(0,item.qty-committed-production)
            for pool in Pool.objects.filter(sku=item.sku).filter(Q(seller=None)|Q(seller=o.seller)).order_by('id'):
                n=min(remaining,pool.stock-pool.reserved)
                if n:
                    pool.reserved+=n; pool.updated_at=timezone.now(); pool.save()
                    Reservation.objects.create(item=item,pool=pool,qty=n)
                    remaining-=n; allocated+=n
            if remaining and item.sku.design_ready:
                Job.objects.create(item=item,sku=item.sku,stage='printing',incoming=remaining)
    return allocated

def eligible_wip(pool):
    jobs=Job.objects.filter(sku=pool.sku).filter(Q(item__order__cancelled=False,item__order__shipped_at=None)|Q(item=None,pool=pool))
    if pool.seller_id:
        jobs=jobs.filter(Q(item__order__seller=pool.seller)|Q(item=None,pool=pool))
    else:
        exclusive=Pool.objects.filter(sku=pool.sku,seller__isnull=False).values('seller')
        jobs=jobs.exclude(item__order__seller__in=exclusive)
    ids=[];qty=0
    for j in jobs:
        ids.append(j.id)
        qty+=j.incoming-j.good-j.scrap
        if j.stage!='qc': qty+=j.good-j.sent
    for t in Transfer.objects.filter(job_id__in=ids): qty+=t.qty-t.received
    return qty

def recommend(pool, forecast, timely_wip=0):
    items=Item.objects.filter(sku=pool.sku,order__cancelled=False,order__shipped_at=None)
    if pool.seller_id: items=items.filter(order__seller=pool.seller)
    else: items=items.exclude(order__seller__in=Pool.objects.filter(sku=pool.sku,seller__isnull=False).values('seller'))
    known=sum(max(0,i.qty-i.ready) for i in items)
    available=pool.stock
    return known,available,restock_qty(known,forecast,available,timely_wip)

def restock_qty(known, forecast, stock, timely_wip):
    return max(0,max(known,forecast)-stock-timely_wip)


@transaction.atomic
def execute(user,d,key):
    action=d.get('action')
    if action not in PERMISSIONS or role(user) not in PERMISSIONS[action]: raise PermissionError('Akses tindakan tidak tersedia untuk peran Anda.')
    if not key or len(key)>100: raise RuleError('Idempotency key diperlukan.')
    fingerprint=hashlib.sha256(json.dumps({'user':user.pk,'data':d},sort_keys=True).encode()).hexdigest()
    guard=Guard.objects.select_for_update().get(pk=1)
    old=Receipt.objects.filter(pk=key).first()
    if old:
        if old.fingerprint!=fingerprint: raise RuleError('Kunci penyimpanan telah dipakai untuk data berbeda.')
        return old.response
    detail=''; performer=str(d.get('performer','')).strip()[:100]
    if action=='create_order':
        seller=Seller.objects.get(pk=d['seller'])
        wb=str(d.get('waybill','')).strip(); ref=str(d.get('source_ref','')).strip()
        if not wb or not ref or len(wb)>100 or len(ref)>100: raise RuleError('Resi dan referensi sumber wajib diisi, maksimal 100 karakter.')
        if Order.objects.filter(Q(waybill=wb)|Q(source_ref=ref)).exists(): raise RuleError('Resi / referensi sudah ada. Periksa order lama; tidak ditimpa.')
        lines=d.get('items',[])
        if not isinstance(lines,list) or not 1<=len(lines)<=30: raise RuleError('Isi 1–30 baris item.')
        pickup=d.get('pickup','16:00')
        if pickup not in ['13:00','16:00','18:00']: raise RuleError('Jadwal pickup tidak valid.')
        order=Order.objects.create(number=f'NCK-{timezone.localdate():%y%m%d}-{Order.objects.count()+1:04}',source_ref=ref,waybill=wb,seller=seller,pickup=pickup,pickup_confirmed=pickup!='18:00')
        for line in lines:
            sku=SKU.objects.get(pk=line['sku']); qty=integer(line,'qty',1)
            Item.objects.create(order=order,sku=sku,qty=qty,cost=sku.cost,cost_version=sku.cost_version,price=sku.price)
        allocate_all(); detail=f'{order.number} • {wb} diterima; alokasi FIFO dijalankan.'
    elif action=='allocate': detail=f'{allocate_all()} pcs berhasil direservasi; antrean produksi diperiksa.'
    elif action in ['pick','pack','ship','cancel','priority']:
        o=Order.objects.get(pk=d['id']); version(o,d)
        if o.cancelled or o.shipped_at: raise RuleError('Order sudah ditutup.')
        if action=='pick':
            rows=list(Reservation.objects.filter(item__order=o,picked=False,released=False))
            if not rows: raise RuleError('Tidak ada reservasi yang dapat dipicking.')
            for r in rows:
                p=r.pool; p.stock-=r.qty; p.reserved-=r.qty; p.updated_at=timezone.now(); p.save()
                r.picked=True; r.save()
                Job.objects.create(item=r.item,sku=r.item.sku,stage='qc',incoming=r.qty)
            detail=f'{o.number}: {sum(r.qty for r in rows)} pcs dipicking ke antrean QC.'
        elif action=='pack':
            if not o.items.exists() or any(i.ready!=i.qty for i in o.items.all()): raise RuleError('Seluruh SKU harus lengkap dan lulus QC sebelum packing.')
            if o.packed: raise RuleError('Paket sudah dipacking.')
            o.packed=True; detail=f'{o.number}: kelengkapan item dan packing dikonfirmasi.'
        elif action=='ship':
            if not o.packed or any(i.ready!=i.qty for i in o.items.all()): raise RuleError('Paket belum lengkap / belum dipacking.')
            evidence=reason(d)
            if o.pickup=='18:00' and not d.get('confirmed'): raise RuleError('Pickup 18.00 wajib dikonfirmasi terlebih dahulu.')
            o.pickup_confirmed=True; o.shipped_at=timezone.now(); o.evidence=evidence
            Pool.objects.filter(sku__in=o.items.values('sku')).filter(Q(seller=None)|Q(seller=o.seller)).update(last_sale=timezone.localdate())
            detail=f'{o.number}: diserahkan ke ekspedisi. Bukti: {evidence}'
        elif action=='cancel':
            why=reason(d); o.cancelled=True
            for r in Reservation.objects.filter(item__order=o,picked=False,released=False):
                p=r.pool; p.reserved-=r.qty;p.save();r.released=True;r.save()
            detail=f'{o.number} batal: {why}. Reservasi belum picked dilepas; WIP dan barang picked tetap tercatat.'
        else: o.priority=not o.priority; detail=f'{o.number}: pengecualian prioritas {o.priority}. Alasan: {reason(d)}'
        o.version+=1;o.save()
    elif action in ['production','qc','rework','transfer','block']:
        j=Job.objects.select_related('item__order','sku').get(pk=d['id']);version(j,d);job_active(j)
        if action=='rework' and ((role(user)=='qc' and j.stage!='qc') or (role(user)=='operator' and j.stage=='qc')): raise PermissionError('Rework QC memerlukan peran QC atau admin.')
        if action=='block': j.blocker=str(d.get('reason','')).strip()[:250];detail=f'{j.sku.code} {j.stage}: hambatan {j.blocker or "diselesaikan"}'
        else:
            if j.blocker: raise RuleError('Selesaikan hambatan sebelum mencatat hasil.')
            if action in ['production','qc']:
                if (j.stage=='qc') != (action=='qc'): raise RuleError('Gunakan pencatatan sesuai tahap dan hak akses QC.')
                if not performer: raise RuleError('Nama pelaksana wajib diisi; pencatat tersimpan terpisah.')
                good=integer(d,'good');hold=integer(d,'hold');scrap=integer(d,'scrap')
                if not good+hold+scrap: raise RuleError('Isi minimal satu hasil.')
                if good+hold+scrap>j.incoming-j.good-j.hold-j.scrap: raise RuleError('Jumlah hasil melebihi input tersedia.')
                if hold+scrap: reason(d)
                j.good+=good;j.hold+=hold;j.scrap+=scrap
                if j.stage=='qc':
                    if j.item:
                        item=j.item;item.ready+=good;item.save();o=item.order;o.version+=1;o.save()
                    else:
                        p=j.pool;p.stock+=good;p.updated_at=timezone.now();p.save()
                detail=f'{j.sku.code} • {j.stage}: {good} baik, {hold} hold, {scrap} scrap. {d.get("reason","")}'
            elif action=='rework':
                n=integer(d,'qty',1)
                if n>j.hold: raise RuleError('Jumlah rework melebihi hold.')
                j.hold-=n;detail=f'{j.sku.code}: {n} hold kembali ke input tahap {j.stage}. {reason(d)}'
            else:
                n=integer(d,'qty',1)
                if not next_stage(j): raise RuleError('Hasil QC tidak memerlukan transfer produksi.')
                if n>j.good-j.sent: raise RuleError('Transfer melebihi hasil baik yang belum dikirim.')
                j.sent+=n;Transfer.objects.create(job=j,qty=n)
                detail=f'{j.sku.code}: {n} pcs dikirim dari {j.stage}; menunggu penerimaan.'
        j.version+=1;j.save()
    elif action=='receive':
        t=Transfer.objects.select_related('job__sku','job__item__order').get(pk=d['id']);j=t.job;job_active(j)
        n=integer(d,'qty',1)
        if n>t.qty-t.received: raise RuleError('Jumlah diterima melebihi sisa transfer.')
        stage=next_stage(j)
        if role(user)=='qc' and stage!='qc': raise PermissionError('Peran QC hanya menerima transfer ke QC.')
        Job.objects.create(item=j.item,pool=j.pool,sku=j.sku,stage=stage,incoming=n)
        t.received+=n;t.save();detail=f'{j.sku.code}: {n} pcs diterima tahap {stage}.'
    elif action=='design':
        s=SKU.objects.get(pk=d['id']);s.design_ready=True;s.save();allocate_all();detail=f'{s.code}: desain siap. {reason(d)}'
    elif action=='restock':
        p=Pool.objects.get(pk=d['id']);forecast=integer(d,'forecast');timely=integer({**{'timely_wip':0},**d},'timely_wip')
        if timely>eligible_wip(p): raise RuleError('WIP tepat waktu melebihi WIP eligible yang tercatat.')
        known,available,qty=recommend(p,forecast,timely)
        if not qty: raise RuleError('Tidak ada kebutuhan restock dari input saat ini.')
        if Decision.objects.filter(pool=p,status='pending').exists(): raise RuleError('Usulan untuk pool ini masih menunggu keputusan.')
        Decision.objects.create(pool=p,forecast=forecast,known=known,available=available,qty=qty,timely_wip=timely,guard_version=guard.version+1,reason=reason(d))
        detail=f'Usulan restock {p.sku.code}: {qty} pcs; forecast total sudah mencakup order terbuka, WIP tepat waktu {timely} pcs dikonfirmasi PPIC untuk horizon 7 hari.'
    elif action in ['approve','reject']:
        dec=Decision.objects.select_related('pool__sku').get(pk=d['id'])
        if dec.status!='pending': raise RuleError('Keputusan ini sudah diproses.')
        why=reason(d)
        if action=='approve':
            if guard.version!=dec.guard_version: raise RuleError('Data berubah sejak usulan. Tolak usulan lama dan hitung ulang agar tidak menyetujui data usang.')
            if not dec.pool.sku.design_ready: raise RuleError('Desain belum siap; jangan mulai produksi restock.')
            Job.objects.create(pool=dec.pool,sku=dec.pool.sku,stage='printing',incoming=dec.qty)
            dec.status='approved'
        else: dec.status='rejected'
        dec.save();detail=f'Restock {dec.pool.sku.code} {dec.qty} pcs: {dec.status}. {why}'
    guard.version+=1;guard.save()
    Audit.objects.create(actor=user.username,performer=performer,action=action,detail=detail)
    response={'message':detail}
    Receipt.objects.create(key=key,fingerprint=fingerprint,response=response)
    return response
