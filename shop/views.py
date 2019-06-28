# -*- coding: utf-8 -*-
# 以下追記9→次はmodels編集
from django.views import generic

from .models import Good
from .forms import GoodSearchForm
from django.db.models import Q


class IndexView(generic.ListView):

    paginate_by = 5
    template_name = 'shop/index.html'
    model = Good


    def post(self, request, *args, **kwargs):
        """
        検索フォームに入力された値をセッションに格納するメソッド
        ⇒初期アクセスでは、検索フォームに入力されていない⇒セッションに格納される処理は呼ばれない
        ⇒初期アクセスではこのメソッドは呼ばれない
        """

        form_value = [
                self.request.POST.get('title', None),
                self.request.POST.get('price', None),
            ]


        request.session['form_value'] = form_value

        # 不明
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        # generic/list.pyのget()メソッドが呼び出される
        return self.get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        """
         初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        context = super().get_context_data(**kwargs)

        title = ''
        price = ''

        # 最初はセッションに値が無いからこのif節は呼ばれない
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            title = form_value[0]
            price = form_value[1]

        # 辞書新規作成⇒初期値ではそれぞれ「空白」が設定
        default_data = {'title' : title, 'price' : price}

        # 入力フォームに空白を設定する処理
        test_form = GoodSearchForm(initial = default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理
        context['test_form'] = test_form
        return context


    def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）

        # セッションに値があるときに動作する
        # ⇒最初にページに入ったときはセッションに値がないので、下のelse文が実行される
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            title = form_value[0]
            price = form_value[1]

            condition_title = Q()
            condition_price = Q()

            if len(title) != 0 and title[0]:
                condition_title = Q(title__contains = title)
            if len(price) != 0 and price[0]:
                condition_price = Q(price__contains = price)

            return Good.objects.select_related().filter(condition_title & condition_price)

        else:
            return Good.objects.none() # 何も返さない

