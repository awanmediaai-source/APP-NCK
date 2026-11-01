import uuid,json
from concurrent.futures import ThreadPoolExecutor
from django.test import TestCase,TransactionTestCase,Client
from django.contrib.auth.models import User
from django.db import connections
from django.utils import timezone
from .models import *
from .services import execute,RuleError,restock_qty

class Fixtures:
    def setup_data(self):
        Guard.objects.create(pk=1)
        self.admin=User.objects.create_user('admin',password='test-password');Profile.objects.create(user=self.admin,role='admin')
        self.operator=User.objects.create_user('operator',password='test-password');Profile.objects.create(user=self.operator,role='operator')
        self.a=Seller.objects.create(name='A');self.b=Seller.objects.create(name='B')
        self.sku=SKU.objects.create(code='SKU-M',name='Demo',category='DTF',size='M',cost=40,price=80)
        self.pool=Pool.objects.create(sku=self.sku,stock=10)
    def order(self,qty=2,seller=None,sku=None):
        key=uuid.uuid4().hex
        o=Order.objects.create(number=key,source_ref=key,waybill=key,seller=seller or self.a)
        Item.objects.create(order=o,sku=sku or self.sku,qty=qty,cost=40,price=80,cost_version='v1')
        return o
    def cmd(self,action,user=None,**data):return execute(user or self.admin,{'action':action,**data},uuid.uuid4().hex)

class DomainTests(Fixtures,TestCase):
    def setUp(self):self.setup_data()
    def test_fifo_and_repeat_allocation(self):
        first=self.order(8);second=self.order(8)
        self.cmd('allocate');self.cmd('allocate')
        self.assertEqual(Reservation.objects.filter(item__order=first).aggregate(n=models.Sum('qty'))['n'],8)
        self.assertEqual(Reservation.objects.filter(item__order=second).aggregate(n=models.Sum('qty'))['n'],2)
        self.assertEqual(Job.objects.get(item__order=second).incoming,6)
        self.pool.refresh_from_db();self.assertEqual(self.pool.reserved,10)
    def test_exclusive_stock_not_used_by_other_seller(self):
        self.pool.seller=self.a;self.pool.save();o=self.order(seller=self.b);self.cmd('allocate')
        self.assertFalse(Reservation.objects.filter(item__order=o).exists())
    def test_idempotency_and_payload_conflict(self):
        self.order();key=uuid.uuid4().hex;d={'action':'allocate'}
        self.assertEqual(execute(self.admin,d,key),execute(self.admin,d,key));self.assertEqual(Audit.objects.count(),1)
        with self.assertRaises(RuleError):execute(self.admin,{'action':'allocate','x':1},key)
    def test_multi_sku_pack_rejected(self):
        o=self.order();i=o.items.get();i.ready=i.qty;i.save();Item.objects.create(order=o,sku=self.sku,qty=1,cost=40,price=80,cost_version='v1')
        with self.assertRaises(RuleError):self.cmd('pack',id=str(o.id),version=o.version)
    def test_partial_output_transfer_ack_and_rework(self):
        o=self.order(100);j=Job.objects.create(item=o.items.get(),sku=self.sku,stage='printing',incoming=100)
        self.cmd('production',id=str(j.id),version=1,good=60,hold=2,scrap=0,performer='B',reason='Uji hold')
        self.cmd('transfer',id=str(j.id),version=2,qty=40)
        self.assertFalse(Job.objects.filter(stage='press').exists());t=Transfer.objects.get()
        self.cmd('receive',id=str(t.id),qty=30);self.assertEqual(Job.objects.get(stage='press').incoming,30)
        self.cmd('rework',id=str(j.id),version=3,qty=2,reason='Cetak ulang')
        self.cmd('production',id=str(j.id),version=4,good=40,hold=0,scrap=0,performer='B')
        j.refresh_from_db();self.assertEqual(j.good,100);self.assertEqual(j.hold,0)
        with self.assertRaises(RuleError):self.cmd('receive',id=str(t.id),qty=11)
    def test_cancel_preserves_picked_and_releases_unused(self):
        a=self.order(3);b=self.order(3);self.cmd('allocate');self.cmd('pick',id=str(a.id),version=1)
        self.cmd('cancel',id=str(a.id),version=2,reason='Uji');self.cmd('cancel',id=str(b.id),version=1,reason='Uji')
        self.pool.refresh_from_db();self.assertEqual(self.pool.stock,7);self.assertEqual(self.pool.reserved,0)
        self.assertTrue(Job.objects.filter(item__order=a).exists())
    def test_oversized_results_and_stale_version(self):
        o=self.order();j=Job.objects.create(item=o.items.get(),sku=self.sku,stage='printing',incoming=2)
        for data in [dict(version=1,good=3),dict(version=0,good=1)]:
            with self.assertRaises(RuleError):self.cmd('production',id=str(j.id),hold=0,scrap=0,performer='B',**data)
    def test_real_handover_required_and_18_confirmed(self):
        o=self.order();o.pickup='18:00';o.save()
        with self.assertRaises(RuleError):self.cmd('ship',id=str(o.id),version=1,reason='Kurir')
        i=o.items.get();i.ready=i.qty;i.save();self.cmd('pack',id=str(o.id),version=1)
        o.refresh_from_db();self.assertIsNone(o.shipped_at)
        with self.assertRaises(RuleError):self.cmd('ship',id=str(o.id),version=2,reason='Kurir')
        self.cmd('ship',id=str(o.id),version=2,reason='Kurir',confirmed=True)
        o.refresh_from_db();self.assertIsNotNone(o.shipped_at)
    def test_permissions_and_financial_api(self):
        self.order()
        with self.assertRaises(PermissionError):self.cmd('allocate',user=self.operator)
        self.client.force_login(self.operator);data=self.client.get('/api/state').json();self.assertNotIn('cost',data['orders'][0]['items'][0]);self.assertEqual(self.client.get('/api/export').status_code,403)
    def test_csrf_and_unauthenticated_commands(self):
        c=Client(enforce_csrf_checks=True);self.assertEqual(c.post('/api/command',data='{}',content_type='application/json').status_code,403)
        self.assertEqual(self.client.get('/api/state').status_code,401)
    def test_restock_formula(self):self.assertEqual(restock_qty(12,20,10,5),5)
    def test_restock_approval_only_once_and_stale(self):
        self.cmd('restock',id=str(self.pool.id),forecast=20,reason='Trend')
        d=Decision.objects.get();self.cmd('approve',id=str(d.id),reason='Review selesai')
        self.assertEqual(Job.objects.count(),1)
        with self.assertRaises(RuleError):self.cmd('approve',id=str(d.id),reason='Review selesai')
        self.cmd('restock',id=str(self.pool.id),forecast=20,reason='Trend');d=Decision.objects.get(status='pending')
        self.cmd('allocate')
        with self.assertRaises(RuleError):self.cmd('approve',id=str(d.id),reason='Data lama')
    def test_duplicate_source_rejected_and_transaction_rollback(self):
        d={'seller':str(self.a.id),'source_ref':'ref','waybill':'resi','items':[{'sku':str(self.sku.id),'qty':2}]}
        self.cmd('create_order',**d)
        with self.assertRaises(RuleError):self.cmd('create_order',**d)
        self.assertEqual(Order.objects.count(),1)
    def test_cost_version_snapshot(self):
        d={'seller':str(self.a.id),'source_ref':'ref','waybill':'resi','items':[{'sku':str(self.sku.id),'qty':2}]}
        self.cmd('create_order',**d);self.sku.cost=99;self.sku.save();self.assertEqual(Item.objects.get().cost,40)
    def test_vendor_partial_does_not_skip_qc(self):
        o=self.order(100);j=Job.objects.create(item=o.items.get(),sku=self.sku,stage='vendor',incoming=100)
        # Vendor belongs to a Jersey route.
        self.sku.category='Jersey';self.sku.save()
        self.cmd('production',id=str(j.id),version=1,good=60,hold=0,scrap=0,performer='Vendor')
        self.cmd('transfer',id=str(j.id),version=2,qty=60);self.cmd('receive',id=str(Transfer.objects.get().id),qty=60)
        qc=Job.objects.get(stage='qc');self.cmd('qc',id=str(qc.id),version=1,good=55,hold=5,scrap=0,performer='QC',reason='Cacat')
        self.assertEqual(o.items.get().ready,55);j.refresh_from_db();self.assertEqual(j.incoming-j.good,40)

class ConcurrencyTests(Fixtures,TransactionTestCase):
    def setUp(self):self.setup_data()
    def test_last_unit_reserved_once(self):
        self.pool.stock=1;self.pool.save();a=self.order(1);b=self.order(1)
        def run(_):
            try:
                u=User.objects.get(pk=self.admin.pk)
                return execute(u,{'action':'allocate'},uuid.uuid4().hex)
            finally:connections.close_all()
        with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,[1,2]))
        self.pool.refresh_from_db();self.assertEqual(self.pool.reserved,1)
        self.assertEqual(Reservation.objects.count(),1);self.assertEqual(Reservation.objects.get().item.order,a)

class RecommendationTests(Fixtures,TestCase):
    def setUp(self):self.setup_data()
    def test_u18_real_recommendation(self):
        o=self.order(12)
        Job.objects.create(item=o.items.get(),sku=self.sku,stage='printing',incoming=5)
        self.cmd('restock',id=str(self.pool.id),forecast=20,timely_wip=5,reason='PPIC konfirmasi selesai 3 hari')
        self.assertEqual(Decision.objects.get().qty,5)
    def test_unrecorded_wip_cannot_reduce_demand(self):
        with self.assertRaises(RuleError):self.cmd('restock',id=str(self.pool.id),forecast=20,timely_wip=5,reason='Belum tercatat')
    def test_wip_not_counted_twice_after_transfer(self):
        from .services import eligible_wip
        o=self.order(10);j=Job.objects.create(item=o.items.get(),sku=self.sku,stage='printing',incoming=10,good=10,sent=6)
        t=Transfer.objects.create(job=j,qty=6,received=4)
        Job.objects.create(item=o.items.get(),sku=self.sku,stage='press',incoming=4)
        self.assertEqual(eligible_wip(self.pool),10)
