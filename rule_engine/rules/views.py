from django.shortcuts import render
from .utils import create_rule, evaluate_rule, combine_rules


def index(request):
    if request.method == "POST":
        rule_string = request.POST.get("rule")
        data_string = request.POST.get("data")

        try:
            data = eval(data_string)  # Convert string to dictionary
            combined_ast = create_rule(rule_string)
            result = evaluate_rule(combined_ast, data)
        except Exception as e:
            result = f"Error: {str(e)}"

        return render(request, 'result.html', {'result': result})

    return render(request, 'index.html')


