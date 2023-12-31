import logging
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Config, Report
from .serializers import CreateConfigSerializer, RetrieveConfigSerializer, CreateReportSerializer, HitMeConfigSerializer
from .utils import get_client_ip

logger = logging.getLogger(__name__)


class ConfigViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Config.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateConfigSerializer
        elif self.action == 'retrieve':
            return RetrieveConfigSerializer
        elif self.action == 'hit_me':
            return HitMeConfigSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(instance.uuid, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def hit_me(self, request, *args, **kwargs):
        ip_observed, ip_client = get_client_ip(request)
        # ...add logic of dynamic scoring here...
        # order by best xray_result and least number of times consumed (previously offered) - limit 2
        configs = Config.objects.filter(xray_result__successful=True) \
                      .order_by("xray_result__avg_latency", 'num_consumed')[:2]
        serializer = self.get_serializer(configs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def stats(self, request):
        total_configs = Config.objects.all().count()
        total_reports = Report.objects.all().count()
        return Response({
            'total_configs': total_configs,
            'total_reports': total_reports
        })

    @action(detail=False, methods=['GET'])
    def ip(self, request):
        return Response(get_client_ip(request), status=status.HTTP_200_OK)


class ReportViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Report.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response("report submitted", status=status.HTTP_201_CREATED)
