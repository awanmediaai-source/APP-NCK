import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta: abstract = True

class Guard(models.Model):
    version = models.PositiveIntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    role = models.CharField(max_length=30, default='operator')

class Seller(Entity):
    name = models.CharField(max_length=150, unique=True)

class SKU(Entity):
    code = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    cost = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    cost_version = models.CharField(max_length=30, default='DEMO-v1')
    price = models.DecimalField(max_digits=14, decimal_places=2)
    design_ready = models.BooleanField(default=True)

class Pool(Entity):
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, null=True)
    stock = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)
    last_sale = models.DateField(null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta:
        constraints=[models.CheckConstraint(condition=models.Q(stock__gte=models.F('reserved')),name='stock_covers_reservations')]

class Order(Entity):
    number = models.CharField(max_length=60, unique=True)
    source_ref = models.CharField(max_length=100, unique=True)
    waybill = models.CharField(max_length=100, unique=True)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT)
    received_at = models.DateTimeField(default=timezone.now)
    pickup = models.CharField(max_length=5, default='16:00')
    pickup_confirmed = models.BooleanField(default=True)
    packed = models.BooleanField(default=False)
    shipped_at = models.DateTimeField(null=True)
    evidence = models.CharField(max_length=250, blank=True)
    cancelled = models.BooleanField(default=False)
    priority = models.BooleanField(default=False)
    blocker = models.CharField(max_length=250, blank=True)
    version = models.PositiveIntegerField(default=1)

class Item(Entity):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    ready = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    cost_version = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    class Meta:
        constraints=[models.CheckConstraint(condition=models.Q(ready__lte=models.F('qty')),name='ready_within_order')]

class Reservation(Entity):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    pool = models.ForeignKey(Pool, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    picked = models.BooleanField(default=False)
    released = models.BooleanField(default=False)

class Job(Entity):
    item = models.ForeignKey(Item, null=True, on_delete=models.PROTECT)
    pool = models.ForeignKey(Pool, null=True, on_delete=models.PROTECT)
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT)
    stage = models.CharField(max_length=20)
    incoming = models.PositiveIntegerField(default=0)
    good = models.PositiveIntegerField(default=0)
    hold = models.PositiveIntegerField(default=0)
    scrap = models.PositiveIntegerField(default=0)
    sent = models.PositiveIntegerField(default=0)
    blocker = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    version = models.PositiveIntegerField(default=1)
    class Meta:
        constraints=[models.CheckConstraint(condition=models.Q(incoming__gte=models.F('good')+models.F('hold')+models.F('scrap')),name='results_within_input'),models.CheckConstraint(condition=models.Q(sent__lte=models.F('good')),name='transfer_within_good')]

class Transfer(Entity):
    job = models.ForeignKey(Job, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    received = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

class Decision(Entity):
    pool = models.ForeignKey(Pool, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    forecast = models.PositiveIntegerField()
    known = models.PositiveIntegerField()
    available = models.PositiveIntegerField()
    timely_wip = models.PositiveIntegerField(default=0)
    guard_version = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='pending')
    reason = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)

class Audit(Entity):
    actor = models.CharField(max_length=100)
    performer = models.CharField(max_length=100, blank=True)
    action = models.CharField(max_length=80)
    detail = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class Receipt(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    fingerprint = models.CharField(max_length=64)
    response = models.JSONField()
