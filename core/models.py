from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# Create your models here.
class Node(MPTTModel):
    time_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=160, null=False)
    description = models.TextField(null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class Meta:
        abstract = True
        get_latest_by = 'time_created'


class Problem(Node):
    class Meta:
        verbose_name = "Problems in South Africa"
        verbose_name_plural = "South Africa's Problems"


class Solution(Node):
    problems = models.ManyToManyField(Problem, related_name='potential_solutions')

    class Meta:
        verbose_name = "Possible Solution to a Problem"
        verbose_name_plural = "Potential Solutions"


class Machine(Node):
    solutions = models.ManyToManyField(Solution, related_name='agents_of_change')
