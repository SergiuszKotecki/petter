# Create your views here.
import datetime

from django import forms
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView

from deals.models import Comment
from deals.models import Deal
from deals.models import Vote


def vote_view(request):
    if request.POST.get('action') == 'votes':

        deal_id = int(request.POST.get('deal_id'))
        user_vote = Vote.objects.filter(Q(user_id=request.user.id) & Q(deal_id=deal_id))
        button = request.POST.get('button')
        success_vote = None

        if not user_vote and button == 'vote_up':
            Vote.objects.create(deal_id=deal_id,
                                user_id=request.user.id,
                                vote_value=Vote.VoteChoice.PLUS)
            success_vote = button
        if not user_vote and button == 'vote_down':
            Vote.objects.create(deal_id=deal_id,
                                user_id=request.user.id,
                                vote_value=Vote.VoteChoice.MINUS)
            success_vote = button
        deal_o = Deal.objects.get(id=deal_id)
        return JsonResponse({'total': deal_o.get_voting_count(),
                             "vote": success_vote})


class DealListView(ListView):
    model = Deal
    template_name = 'deals/deal_list.html'
    context_object_name = 'deals'
    paginate_by = 5
    ordering = ['-created_at']


class DealCreateView(CreateView):
    model = Deal
    template_name = 'deals/deal_create.html'
    fields = ['name', 'description', 'link', 'product_img',
              'current_price', 'historical_price', 'delivery_cost',
              # 'valid_till' commented for mocking purpose
              ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        today = datetime.date.today()
        form.instance.valid_till = today + datetime.timedelta(8)
        return super().form_valid(form)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-3', 'id': 'comment_id'}))


class NewDealDetailView(DetailView):
    model = Deal
    context_object_name = 'deal'

    def can_vote(self):
        ...

    def get_context_data(self, **kwargs):
        context = super(NewDealDetailView, self).get_context_data(**kwargs)
        context.update({
            'form': CommentForm()
        })
        comments = Comment.objects.filter(deal_id=self.object.id).order_by('-created_at')[:10]
        votes = Vote.objects.filter(deal_id=self.object.id)
        have_voted = votes.filter(user_id=self.request.user.id).exists()
        if have_voted:
            have_voted = votes.get(user_id=self.request.user.id)
        context['have_voted'] = have_voted
        context['comments'] = comments
        context['votes'] = votes
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object(self.get_queryset())
        form = CommentForm(self.request.POST)
        print(form)
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.deal = self.object
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(**kwargs)
            context.update({'form': form})
            return self.render_to_response(context)


class DealDeleteView(DeleteView):
    model = Deal
    success_url = reverse_lazy("deals:list")
    template_name_suffix = "_delete"
