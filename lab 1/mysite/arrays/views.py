from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from arrays.generators.generators import Zero_FiftyGenerator_1D, IntegerGenerator_1D, FloatGenerator_1D, \
    IntegerGenerator_2D, FloatGenerator_2D, task_1, task_2


def index(request):
    if request.method =='GET':
        return render(request, 'arrays/index.html')
    else:
        v = request.POST['choice']
        if v == '1d':
            return render(request, 'arrays/set_up_1.html')
        elif v == '2d':
            return render(request, 'arrays/set_up_2.html')

def data(request, d):
    if request.method == 'POST':
        n = int(request.POST['n'])
        min_val = int(request.POST['min_val'])
        max_val = int(request.POST['max_val'])
        _type = request.POST['_type']
        arr = [1, 2,3]
        farr = [1, 2,3]
        if d == 1:
            if _type == 'i':
                IntegerGenerator_1D.init()
                arr = IntegerGenerator_1D.generate(min_val, max_val, n)
            if _type == 'f':
                FloatGenerator_1D.init()
                arr = FloatGenerator_1D.generate(min_val, max_val, n)
            farr = task_1(arr)
        if d == 2:
            m = int(request.POST['m'])
            if _type == 'i':
                IntegerGenerator_2D.init()
                arr = IntegerGenerator_2D.generate(min_val, max_val, n, m)
            if _type == 'f':
                FloatGenerator_2D.init()
                arr = FloatGenerator_2D.generate(min_val, max_val, n, m)
            farr = task_2(arr)
        arr = arr.tolist()
        return render(request, 'arrays/data.html/', context={'dim':d, 'array': arr, 'f_array':farr})

