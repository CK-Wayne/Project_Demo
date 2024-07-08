from django.shortcuts import render
from .models import User, Item
from django.db.models import Max

def show_scores(request):
    max_user_id = User.objects.aggregate(max_id=Max('user_id'))['max_id']
    # 檢查是否有查詢參數
    if request.method == 'POST':
        mode = request.POST.get('mode', 'top_k')
        k = (request.POST.get('k', 5))
        try:
            k = int(k)
        except ValueError:
            k = 5
        context = {'max_user_id': max_user_id}

        if mode == 'specific_user':
            user_id = (request.POST.get('user_id', '0'))
            threshold_str = request.POST.get('threshold', '0.1546')  # 獲取threshold字符串
            try:
                threshold = float(threshold_str)  # 嘗試轉換為float
            except ValueError:
                threshold = 0.1546  # 如果轉換失敗，使用預設值
            if user_id:
                user_score = User.objects.filter(user_id=user_id).first()
                if user_score:
                    results = [{'user_id': user_score.user_id, 'result': 1 if user_score.anomaly_score > threshold else 0}]
                    context['results'] = results
                    context['selected_mode'] = 'specific_user'
        else:
            top_k_users = User.objects.order_by('-anomaly_score')[:k]
            top_k_items = Item.objects.order_by('-anomaly_score')[:k]
            context['k'] = k
            context['top_k_users'] = top_k_users
            context['top_k_items'] = top_k_items
            context['selected_mode'] = 'top_k'

        return render(request, 'scoreapp/scores.html', context)
    else:
        # 如果沒有查詢參數，返回一個空的context
        return render(request, 'scoreapp/scores.html', {'max_user_id': max_user_id, 'selected_mode': 'specific_user'})