from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by("-id")
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        qp = self.request.query_params

        company = qp.get("company")
        role = qp.get("role")
        status = qp.get("status")

        if company:
            qs = qs.filter(company__icontains=company)
        if role:
            qs = qs.filter(role__icontains=role)
        if status:
            qs = qs.filter(status=status)

        return qs

    @action(detail=False, methods=["get"])
    def stats(self, request):
        qs = Application.objects.all()
        total = qs.count()

        counts = qs.values("status").annotate(c=Count("id"))
        data = {"total": total}
        for row in counts:
            data[row["status"]] = row["c"]

        for s in ["applied", "interview", "offer", "rejected"]:
            data.setdefault(s, 0)

        return Response(data)
