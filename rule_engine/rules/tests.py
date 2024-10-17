from django.test import TestCase
from .models import Node
from .utils import create_rule, evaluate_rule


class RuleEngineTests(TestCase):

    def setUp(self):
        self.node1 = create_rule("age > 30")
        self.node2 = create_rule("income < 50000")

    def test_create_rule(self):
        self.assertIsNotNone(self.node1)
        self.assertEqual(self.node1.value, "age > 30")

    def test_evaluate_rule(self):
        data = {"age": 35, "income": 40000}
        result = evaluate_rule(self.node1, data)
        self.assertTrue(result)

        result = evaluate_rule(self.node2, data)
        self.assertTrue(result)

    def test_invalid_rule(self):
        data = {"age": 25, "income": 60000}
        result = evaluate_rule(self.node1, data)
        self.assertFalse(result)

        result = evaluate_rule(self.node2, data)
        self.assertFalse(result)

