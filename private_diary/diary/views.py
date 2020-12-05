import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm,DiaryCreateForm
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
    #1ページに表示する数を表示する
    paginate_by =2

    def get_queryset(self):
        #self.request.userはログインしているユーザーをのインスタンスを取得
        #-created_atで作成日時を降順で並び替えている
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

class DiaryDetailView(LoginRequiredMixin,generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'

class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    #urlが動的に動く場合につかう
    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)

class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)
