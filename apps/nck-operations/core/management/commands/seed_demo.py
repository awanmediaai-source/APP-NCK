from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from core.models import *
from core.services import allocate_all

class Command(BaseCommand):
    help='Create labeled demo dataset once; does not overwrite existing data.'
    @transaction.atomic
    def handle(self,*args,**opts):
        if Order.objects.exists():
            self.stdout.write('Data sudah ada. Seed tidak dijalankan ulang.');return
        Guard.objects.get_or_create(pk=1)
        for username,name in [('admin','Admin NCK'),('warehouse','Dina Gudang'),('operator','Raka Produksi'),('qc','Sari QC'),('finance','Finance NCK'),('management','Manajemen NCK')]:
            u,_=User.objects.get_or_create(username=username,defaults={'first_name':name});u.set_password('nck-demo-2026');u.save();Profile.objects.get_or_create(user=u,defaults={'role':username})
        sellers=[Seller.objects.create(name=n) for n in ['Awan Media Indonesia (Demo)','Langit Apparel (Demo)','Ruang Jersey (Demo)']]
        specs=[('DTF-WAVE-M','Wave Club Tee','DTF','M',45000,79000,24),('DTF-WAVE-L','Wave Club Tee','DTF','L',45000,79000,16),('JR-GARUDA-M','Garuda Home Jersey','Jersey','M',None,125000,0),('JR-GARUDA-L','Garuda Home Jersey','Jersey','L',68000,125000,6),('DTF-ORBIT-XL','Orbit Graphic Tee','DTF','XL',49000,89000,8),('JR-RETRO-L','Retro Away Jersey','Jersey','L',72000,139000,32),('DTF-NEON-M','Neon Weekend Tee','DTF','M',47000,85000,0),('DTF-BASIC-L','Essential Black Tee','DTF','L',39000,69000,40)]
        skus=[];pools=[]
        for idx,(code,name,cat,size,cost,price,stock) in enumerate(specs):
            s=SKU.objects.create(code=code,name=name,category=cat,size=size,cost=cost,price=price,design_ready=idx!=6);skus.append(s)
            pools.append(Pool.objects.create(sku=s,stock=stock,seller=sellers[0] if idx==4 else None,last_sale=timezone.localdate()-timedelta(days=73 if idx==5 else 2)))
        now=timezone.localtime();base=now.replace(hour=9,minute=0,second=0,microsecond=0)
        def order(idx,lines,days=0,shipped=False,pickup='16:00'):
            t=base-timedelta(days=days)+timedelta(minutes=idx*7)
            o=Order.objects.create(number=f'NCK-{timezone.localdate():%y%m%d}-{idx:04}',source_ref=f'DEMO-SOURCE-{idx}',waybill=f'DEMO-JNE-2601{idx:04}',seller=sellers[idx%3],received_at=t,pickup=pickup,pickup_confirmed=pickup!='18:00',packed=shipped,shipped_at=t+timedelta(hours=3) if shipped else None)
            for si,qty in lines:
                s=skus[si];Item.objects.create(order=o,sku=s,qty=qty,ready=qty if shipped else 0,cost=s.cost,cost_version=s.cost_version,price=s.price)
            return o
        for idx in range(1,15):order(idx,[(idx%2,2+idx%4)],days=1+(idx%6),shipped=idx%4!=0)
        # Historical pending orders are maintained, not hidden by today's KPI scope.
        a=order(15,[(0,4),(1,3)]);b=order(16,[(2,12)],pickup='13:00');c=order(17,[(6,8)]);d=order(18,[(4,5)],pickup='18:00');e=order(19,[(7,6)]);f=order(20,[(0,2)],shipped=True)
        allocate_all()
        # Move one order through an authentic stock -> QC -> packed example.
        for r in Reservation.objects.filter(item__order=e):
            p=r.pool;p.stock-=r.qty;p.reserved-=r.qty;p.save();r.picked=True;r.save()
            Job.objects.create(item=r.item,sku=r.item.sku,stage='qc',incoming=r.qty,good=r.qty)
            i=r.item;i.ready+=r.qty;i.save()
        e.packed=True;e.save()
        # Jersey already in vendor process, represented by distinct physical stages.
        root=Job.objects.filter(item__order=b,stage='printing').first()
        if root:
            root.good=12;root.sent=12;root.save()
            for stage in ['press','cutting']:
                Job.objects.create(item=root.item,sku=root.sku,stage=stage,incoming=12,good=12,sent=12)
            Job.objects.create(item=root.item,sku=root.sku,stage='vendor',incoming=12,good=4,sent=4)
            Job.objects.create(item=root.item,sku=root.sku,stage='qc',incoming=4,good=3,hold=1)
            i=root.item;i.ready=3;i.save()
        Decision.objects.create(pool=pools[1],qty=12,forecast=28,known=7,available=16,guard_version=0,reason='Contoh usulan: kebutuhan 7 hari dari peninjauan PPIC. Tinjau tren sebelum produksi.')
        Audit.objects.create(actor='seed_demo',action='seed',detail='Dataset contoh NCK dibuat. Nama, volume, biaya, dan performa ini bukan data operasional nyata.')
        self.stdout.write(self.style.SUCCESS('Data contoh dan 6 akun demo siap.'))
