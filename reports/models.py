from django.db import models
from accounts.models import Ph


class ReportManager(models.Manager):
    def create_report(self, report_number, ph):
        report = self.create(report_number=report_number, ph=ph)
        report.ph_employee_id = ph.employee_id
        report.ph_employee_ifs = ph.employee_ifs
        report.save()
        return report


class Report(models.Model):
    report_number = models.CharField(max_length=20, unique=True)
    ph = models.ForeignKey(Ph, on_delete=models.CASCADE)
    ph_employee_id = models.CharField(blank=True, null=True)
    ph_employee_ifs = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entry_date = models.DateField(null=True, blank=True)

    def get_report(self):
        related_models = {}

        for model in BaseReport.__subclasses__():
            related_objects = model.objects.filter(report=self).first()

            if related_objects:
                related_models[model.__name__] = related_objects.value

        return related_models

    objects = ReportManager()


class BaseReport(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()


# OL
class OL_Mini(BaseReport):
    pass


class OL_Standard(BaseReport):
    pass


class OL_Extra(BaseReport):
    pass


class OL_F(BaseReport):
    pass


# B2B B2C
class Plan_S(BaseReport):
    pass


class Plan_M(BaseReport):
    pass


class Plan_L(BaseReport):
    pass


class Plan_FS(BaseReport):
    pass


class Plan_FM(BaseReport):
    pass


class Plan_FL(BaseReport):
    pass


class Plan_FXL(BaseReport):
    pass


# HOME
class LTE(BaseReport):
    pass


class XDSL(BaseReport):
    pass


class FTTH(BaseReport):
    pass


class MV_TO_FBB(BaseReport):
    pass


class LTE_B(BaseReport):
    pass


class XDSL_B(BaseReport):
    pass


class FTTH_B(BaseReport):
    pass


class MV_TO_FBB_B(BaseReport):
    pass


class Home_points(BaseReport):
    pass


# TV
class Netflix(BaseReport):
    pass


class Eleven(BaseReport):
    pass


class Canal_p(BaseReport):
    pass


# Additions
class Terminal(BaseReport):
    pass


class MO(BaseReport):
    pass


class OSP(BaseReport):
    pass


class PB(BaseReport):
    pass


class OSPX2(BaseReport):
    pass


class Retention(BaseReport):
    pass
