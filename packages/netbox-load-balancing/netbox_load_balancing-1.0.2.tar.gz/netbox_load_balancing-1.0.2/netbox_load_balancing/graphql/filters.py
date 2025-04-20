import strawberry_django

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

from netbox_load_balancing.models import (
    LBService,
    Listener,
    HealthMonitor,
    Pool,
    Member,
    VirtualIPPool,
    VirtualIP,
)

from netbox_load_balancing.filtersets import (
    LBServiceFilterSet,
    ListenerFilterSet,
    HealthMonitorFilterSet,
    PoolFilterSet,
    MemberFilterSet,
    VirtualIPPoolFilterSet,
    VirtualIPFilterSet,
)


@strawberry_django.filter(LBService, lookups=True)
@autotype_decorator(LBServiceFilterSet)
class NetBoxLoadBalancingLBServiceFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(Listener, lookups=True)
@autotype_decorator(ListenerFilterSet)
class NetBoxLoadBalancingListenerFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(HealthMonitor, lookups=True)
@autotype_decorator(HealthMonitorFilterSet)
class NetBoxLoadBalancingHealthMonitorFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(Pool, lookups=True)
@autotype_decorator(PoolFilterSet)
class NetBoxLoadBalancingPoolFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(Member, lookups=True)
@autotype_decorator(MemberFilterSet)
class NetBoxLoadBalancingMemberFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(VirtualIPPool, lookups=True)
@autotype_decorator(VirtualIPPoolFilterSet)
class NetBoxLoadBalancingVirtualIPPoolFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(VirtualIP, lookups=True)
@autotype_decorator(VirtualIPFilterSet)
class NetBoxLoadBalancingVirtualIPFilter(BaseFilterMixin):
    pass
