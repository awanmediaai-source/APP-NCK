import json,csv,io
from datetime import timedelta
from decimal import Decimal
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.db import IntegrityError
from django.utils import timezone
from .models import *
from .services import execute,RuleError,role,FINANCE,recommend,eligible_wip

def iso(t): return timezone.localtime(t).isoformat() if t else None

def status(o):
    if o.cancelled:return 'Dibatalkan'
    if o.shipped_at:return 'Terkirim'
    if o.packed:return 'Siap pickup'
    if all(i.ready==i.qty for i in o.items.all()):return 'Siap packing'
    if o.blocker:return 'Terhambat'
    return 'Diproses'

@ensure_csrf_cookie
def index(request):
    return render(request,'index.html',{'logged_in':request.user.is_authenticated})

@require_POST
def signin(request):
    try:d=json.loads(request.body)
    except ValueError:return JsonResponse({'error':'Data tidak valid'},status=400)
    user=authenticate(request,username=d.get('username'),password=d.get('password'))
    if not user:return JsonResponse({'error':'Nama akun atau kata sandi salah.'},status=400)
    login(request,user);return JsonResponse({'message':'Berhasil masuk'})

@require_POST
def signout(request):
    logout(request);return JsonResponse({'message':'Keluar'})

@require_POST
def command(request):
    if not request.user.is_authenticated:return JsonResponse({'error':'Silakan masuk kembali.'},status=401)
    try:
        d=json.loads(request.body)
        result=execute(request.user,d,request.headers.get('Idempotency-Key'))
        return JsonResponse(result)
    except PermissionError as e:return JsonResponse({'error':str(e)},status=403)
    except (RuleError,ValueError,KeyError,TypeError,ValidationError,ObjectDoesNotExist,IntegrityError) as e:
        msg=str(e) if isinstance(e,RuleError) else 'Data tidak valid atau sudah tersimpan. Muat ulang dan periksa isian.'
        return JsonResponse({'error':msg},status=400)

def state(request):
    if not request.user.is_authenticated:return JsonResponse({'error':'Silakan masuk.'},status=401)
    financial=role(request.user) in FINANCE
    orders=[];today=timezone.localdate()
    for o in Order.objects.select_related('seller').prefetch_related('items__sku').order_by('-priority','received_at'):
        lines=[]
        for i in o.items.all():
            row={'id':str(i.id),'sku':str(i.sku_id),'code':i.sku.code,'name':i.sku.name,'size':i.sku.size,'qty':i.qty,'ready':i.ready,'design_ready':i.sku.design_ready}
            if financial:row.update(price=str(i.price),cost=str(i.cost) if i.cost is not None else None,cost_version=i.cost_version)
            lines.append(row)
        orders.append({'id':str(o.id),'number':o.number,'waybill':o.waybill,'seller':o.seller.name,'received':iso(o.received_at),'shipped':iso(o.shipped_at),'status':status(o),'pickup':o.pickup,'confirmed':o.pickup_confirmed,'priority':o.priority,'blocker':o.blocker,'version':o.version,'items':lines,'qty':sum(i['qty'] for i in lines),'ready':sum(i['ready'] for i in lines),'pickable':sum(r.qty for r in Reservation.objects.filter(item__order=o,picked=False,released=False)),'evidence':o.evidence})
    pools=[]
    for p in Pool.objects.select_related('sku','seller'):
        pools.append({'id':str(p.id),'sku':str(p.sku_id),'code':p.sku.code,'name':p.sku.name,'category':p.sku.category,'size':p.sku.size,'seller':p.seller.name if p.seller else None,'wip':eligible_wip(p),'stock':p.stock,'reserved':p.reserved,'available':p.stock-p.reserved,'last_sale':str(p.last_sale) if p.last_sale else None,'age':(today-p.last_sale).days if p.last_sale else None,'updated':iso(p.updated_at),'design_ready':p.sku.design_ready})
    jobs=[]
    for j in Job.objects.select_related('sku','item__order','pool').order_by('created_at'):
        jobs.append({'id':str(j.id),'code':j.sku.code,'name':j.sku.name,'stage':j.stage,'incoming':j.incoming,'good':j.good,'hold':j.hold,'scrap':j.scrap,'sent':j.sent,'remaining':j.incoming-j.good-j.hold-j.scrap,'blocker':j.blocker,'version':j.version,'order':j.item.order.number if j.item else 'Restock disetujui','closed':j.item.order.cancelled if j.item else False,'created':iso(j.created_at),'category':j.sku.category})
    transfers=[{'id':str(t.id),'job':str(t.job_id),'code':t.job.sku.code,'from':t.job.stage,'qty':t.qty,'received':t.received} for t in Transfer.objects.select_related('job__sku').filter(received__lt=models.F('qty'))]
    decisions=[{'id':str(d.id),'code':d.pool.sku.code,'qty':d.qty,'timely_wip':d.timely_wip,'forecast':d.forecast,'known':d.known,'available':d.available,'reason':d.reason,'status':d.status,'stale':d.guard_version!=Guard.objects.get(pk=1).version,'created':iso(d.created_at)} for d in Decision.objects.select_related('pool__sku').order_by('-created_at')]
    audits=[{'actor':a.actor,'performer':a.performer,'action':a.action,'detail':a.detail,'time':iso(a.created_at)} for a in Audit.objects.order_by('-created_at')[:80]]
    # Operational audit contains no costs; financial data is excluded at the server boundary.
    skus=[{'id':str(s.id),'code':s.code,'name':s.name,'category':s.category,'size':s.size} for s in SKU.objects.all()]
    return JsonResponse({'user':{'name':request.user.first_name or request.user.username,'username':request.user.username,'role':role(request.user)},'financial':financial,'orders':orders,'pools':pools,'jobs':jobs,'transfers':transfers,'decisions':decisions,'audits':audits,'sellers':list(Seller.objects.values('id','name')),'skus':skus,'now':iso(timezone.now()),'today':str(today),'demo':True})

def export(request):
    if not request.user.is_authenticated:return JsonResponse({'error':'Silakan masuk'},status=401)
    if role(request.user) not in FINANCE:return JsonResponse({'error':'Ekspor keuangan hanya admin, finance, dan manajemen.'},status=403)
    out=io.StringIO();w=csv.writer(out);w.writerow(['DATA CONTOH — NCK; estimasi bukan laba bersih'])
    w.writerow(['Order','Seller','Resi','Status','Nilai order','Estimasi HPP','Cakupan biaya'])
    def safe(v):
        s=str(v)
        return "'"+s if s.startswith(('=','+','-','@','\t','\r')) else s
    for o in Order.objects.select_related('seller').prefetch_related('items'):
        rows=list(o.items.all());complete=all(i.cost is not None for i in rows)
        w.writerow([safe(o.number),safe(o.seller.name),safe(o.waybill),status(o),sum(i.price*i.qty for i in rows),sum(i.cost*i.qty for i in rows) if complete else '', 'Standar DEMO, belum aktual' if complete else 'Belum lengkap'])
    response=HttpResponse('\ufeff'+out.getvalue(),content_type='text/csv; charset=utf-8');response['Content-Disposition']='attachment; filename="NCK-DATA-CONTOH.csv"';return response
