from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permissions import HasPermission


class BooksListView(APIView):
    permission_classes = [HasPermission("read:books")]

    def get(self, request):
        data = [
            {"id": 1, "title": "Война и мир", "author": "Л. Толстой"},
            {"id": 2, "title": "1984", "author": "Дж. Оруэлл"},
        ]
        return Response(data)


class OrdersListView(APIView):
    permission_classes = [HasPermission("read:orders")]

    def get(self, request):
        data = [
            {"id": "ORD-001", "amount": 1500, "status": "completed"},
            {"id": "ORD-002", "amount": 3200, "status": "pending"},
        ]
        return Response(data)
    