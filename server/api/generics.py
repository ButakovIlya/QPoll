from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.cache import cache

from api.exсeptions import *
from api.permissions import IsOwnerOrReadOnly
from api.utils import get_paginated_response, get_object_or_404

from .serializers import *
from .models import *

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser


class CRUDapi(RetrieveUpdateDestroyAPIView):
    model = None
    serializer_class = None
    mini_serializer_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    order_by = 'id'

    queryset = None

    model_type_model = None
    model_type_model_field = None
    model_type_model_url_kwarg  = None

    put_action_name = 'request_type'


    http_method_names = ['get', 'post', 'patch', 'put', 'delete']

    def get_profile(self):
        current_user = self.request.user
        return get_object_or_404(Profile, user=current_user) if not isinstance(current_user, AnonymousUser) else None
    
    def get_profile_to_context(self):
        profile = self.get_profile()
        return {'profile': profile} if profile else {}

    def get_serializer_class(self):
        if self.request.query_params.get(self.lookup_url_kwarg, None):
            return self.serializer_class

        return self.mini_serializer_class
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.get_serializer_class()(*args, **kwargs)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.get_profile_to_context())
        return context


    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE', 'POST', 'PUT']:
            self.permission_classes = [IsOwnerOrReadOnly]
        return super().get_permissions()

    def get_queryset(self):
        if not self.model:
            raise AssertionError("Необходимо указать Модель.")

        queryset = self.queryset if self.queryset is not None else self.model.objects.all()

        filter_params = self.request.query_params.dict()
        filter_params.pop('page', None)
        filter_params.pop('page_size', None)
        filter_params.pop(self.lookup_url_kwarg, None)

        filters = Q()

        filter_fields = getattr(self.model._meta, 'filter_fields', [])


        for field in filter_fields:
            value = filter_params.get(field, None)
            if value:
                if field == self.model_type_model_url_kwarg:
                    model_type = self.model_type_model.objects.filter(name=value).first()
                    if not model_type:
                        raise ObjectNotFoundException(model=self.model_type_model)
                    filters &= Q(**{self.model_type_model_field: model_type})
                elif field == 'name':
                    filters &= Q(name__icontains=value)
                else:
                    filters &= Q(**{field: value})

        queryset = queryset.filter(filters)
        return queryset

    def get_object(self):
        lookup_url_kwarg_data = self.request.query_params.get(self.lookup_url_kwarg)
        if lookup_url_kwarg_data:
            try:
                return self.get_queryset().get(**{self.lookup_field: lookup_url_kwarg_data})
            except self.model.DoesNotExist:
                raise InstanceNotFoundException(model=self.model)
        else:
            raise MissingFieldException(field_name=self.lookup_url_kwarg)


    def get(self, request, *args, **kwargs):
        if self.request.query_params.get(self.lookup_url_kwarg):
            instance = self.get_object()
            if not instance:
                raise InstanceNotFoundException(model=self.model)
        
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset().order_by(self.order_by)
            pagination_data = get_paginated_response(request, queryset, self.get_serializer_class(),
                                                     context=self.get_serializer_context())
            return Response(pagination_data, status=status.HTTP_200_OK)
   
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)

        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            raise InstanceNotFoundException(model=self.model)
        
        self.check_object_permissions(request, instance)

        instance_data = instance
        instance.delete()
        return Response(f"{instance_data} успешно удален.", status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        data = request.data
        request_type = self.get_parameter_or_400(self.put_action_name)


    def get_parameter_or_400(self, parameter_field_name):
        parameter_field = self.request.query_params.get(parameter_field_name, None)
        if not parameter_field:
            raise MissingParameterException(parameter_field_name)
        
        return parameter_field

    def handle_exception(self, exc):
        if isinstance(exc, APIException):
            return Response({'message': f"{exc}"}, exc.status_code)
        logger.error(f"Внутренняя ошибка сервера в poll: {exc}")
        return Response(f"Внутренняя ошибка сервера в {self.__class__.__name__}: {exc}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
