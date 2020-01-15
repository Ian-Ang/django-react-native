from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from Equipment.models import Equipment, Locate
from Equipment.api.serializers import EquipmentSerializer, LocateSerializer

class EquipmentList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        equipment = self.get_object(pk)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        equipment = self.get_object(pk)
        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        equipment = self.get_object(pk)
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LocateList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        locate = Locate.objects.all()
        serializer = LocateSerializer(locate, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LocateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocateDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Locate.objects.get(pk=pk)
        except Locate.DoesNotExist :
            raise Http404

    def get(self, request, pk, format=None):
        locate = self.get_object(pk)
        serializer = LocateSerializer(locate)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        locate = self.get_object(pk)
        serializer = LocateSerializer(locate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        locate = self.get_object(pk)
        locate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
