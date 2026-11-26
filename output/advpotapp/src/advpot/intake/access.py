from django.db.models import Q
from .models import BusinessAssignment, BusinessAuthority, Contact, ContactGrant, Demand, DemandGrant, name_fingerprint


def departments(user):
    if not user.is_authenticated or not user.is_active:
        return set()
    return set(BusinessAssignment.objects.filter(user=user).values_list('department', flat=True))


def is_authority(user):
    return bool(user.is_authenticated and user.is_active and BusinessAuthority.objects.filter(user=user).exists())


def can_create(user):
    return bool(departments(user) & {'secretariat', 'commercial'})


def visible_contacts(user, action='view'):
    if not departments(user):
        return Contact.objects.none()
    if action == 'edit' and not can_create(user):
        return Contact.objects.none()
    queryset = Contact.objects.filter(pk__in=ContactGrant.objects.filter(user=user, action='view').values('contact_id'))
    if action != 'view':
        queryset = queryset.filter(pk__in=ContactGrant.objects.filter(user=user, action=action).values('contact_id'))
    return queryset


def visible_demands(user, action='view'):
    memberships = departments(user)
    if not memberships:
        return Demand.objects.none()
    if action == 'manage_opportunity' and 'commercial' not in memberships:
        return Demand.objects.none()
    queryset = Demand.objects.filter(pk__in=DemandGrant.objects.filter(user=user, action='view').values('demand_id'))
    if action == 'edit_intake' and 'secretariat' not in memberships:
        if 'commercial' not in memberships:
            return Demand.objects.none()
        queryset = queryset.filter(created_by=user, responsible=user, journey_stage='reception')
    if action != 'view':
        queryset = queryset.filter(pk__in=DemandGrant.objects.filter(user=user, action=action).values('demand_id'))
    return queryset


def recoverable_demands(user):
    records = Demand.objects.filter(recovery_queue__isnull=False)
    if is_authority(user):
        return records
    if 'management' in departments(user):
        return records.filter(pk__in=DemandGrant.objects.filter(user=user, action='recover').values('demand_id'))
    return Demand.objects.none()


def recovery_candidates(demand):
    from advpot.identity.models import User
    required = 'edit_intake' if demand.journey_stage == 'reception' else 'manage_opportunity'
    eligible = BusinessAssignment.objects.filter(department='secretariat' if required == 'edit_intake' else 'commercial')
    sectors = Q(pk__in=eligible.values('user_id'))
    if required == 'edit_intake':
        sectors |= Q(pk=demand.created_by_id, pk__in=BusinessAssignment.objects.filter(department='commercial').values('user_id'))
    return User.objects.filter(sectors, is_active=True, pk__in=DemandGrant.objects.filter(demand=demand, action='view').values('user_id')).filter(pk__in=DemandGrant.objects.filter(demand=demand, action=required).values('user_id')).order_by('username')


def possible_duplicates(user, *, name, email='', phone=''):
    matches = Q(name_key=name_fingerprint(name))
    if email.strip():
        matches |= Q(email__iexact=email.strip())
    if phone.strip():
        matches |= Q(phone=phone.strip())
    return visible_contacts(user).filter(matches)
