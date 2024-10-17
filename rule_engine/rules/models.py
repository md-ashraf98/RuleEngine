from django.db import models
import json

class Node(models.Model):
    NODE_TYPE_CHOICES = (
        ('operator', 'Operator'),
        ('operand', 'Operand'),
    )

    type = models.CharField(max_length=10, choices=NODE_TYPE_CHOICES)
    value = models.TextField(null=True, blank=True)  # Optional value for operand nodes
    left = models.ForeignKey('self', null=True, blank=True, related_name='left_child', on_delete=models.CASCADE)
    right = models.ForeignKey('self', null=True, blank=True, related_name='right_child', on_delete=models.CASCADE)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        node_dict = {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
        }
        return node_dict


