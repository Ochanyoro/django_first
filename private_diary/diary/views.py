import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm, DiaryCreateForm
from .models import Diary

logger = logging.getLogger(__name__)



class IndexView(generic.TemplateView):
    template_name = "index.html"

#問い合わせフォームはデータベースを使わないのでFormViewを継承
class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    #InquiryFormとInquiryViewをひもずけるためオーバーライド
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    #この関数は親クラスで定義されており問題がなかったら実行される
    #form:フォームバリデーションを通ったユーザ入力値を取り出す
    def form_valid(self, form):
        form.send_email()
        #メッセージの表示
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

#テーブルをリストアップして表示するのでListViewを継承する
#LoginRequiredMixinを継承することでログインしていないとアクセスできないようにしている
class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'

    def get_queryset(self):
        #self.request.userはログインしているユーザーをのインスタンスを取得
        #-created_atで作成日時を降順で並び替えている
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries
