from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Record
from .serializers import RecordSerializer
from .permissions import IsAdmin, IsAnalystOrAdmin


# ✅ CREATE + LIST
class RecordListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = Record.objects.filter(user=request.user)
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only admin can create
        if request.user.userprofile.role != 'admin':
            return Response({"error": "Only admin can create records"}, status=403)

        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


# ✅ UPDATE + DELETE
class RecordDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return Record.objects.get(pk=pk, user=user)

    def put(self, request, pk):
        if request.user.userprofile.role != 'admin':
            return Response({"error": "Only admin can update"}, status=403)

        record = self.get_object(pk, request.user)
        serializer = RecordSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        if request.user.userprofile.role != 'admin':
            return Response({"error": "Only admin can delete"}, status=403)

        record = self.get_object(pk, request.user)
        record.delete()
        return Response({"message": "Deleted"})
    
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = Record.objects.filter(user=request.user)

        total_income = records.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = records.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense
        })
    