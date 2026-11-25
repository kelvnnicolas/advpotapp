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
    if action == 'edit_intake' and 'secretariat' not in memberships:
        return Demand.objects.none()
    if action == 'manage_opportunity' and 'commercial' not in memberships:
        return Demand.objects.none()
    queryset = Demand.objects.filter(pk__in=DemandGrant.objects.filter(user=user, action='view').values('demand_id'))
    if action != 'view':
        queryset = queryset.filter(pk__in=DemandGrant.objects.filter(user=user, action=action).values('demand_id'))
    return queryset


def possible_duplicates(user, *, name, email='', phone=''):
    matches = Q(name_key=name_fingerprint(name))
    if email.strip():
        matches |= Q(email__iexact=email.strip())
    if phone.strip():
        matches |= Q(phone=phone.strip())
    return visible_contacts(user).filter(matches)
