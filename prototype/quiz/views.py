from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Landmark, Choice
from django.urls import reverse

def index(request):
    '''
    Returns template of last two questions
    '''

    landmarks = Landmark.objects.all()
    template = loader.get_template('quiz/index.html')
    context = {
        'landmarks': landmarks,
    }
    return HttpResponse(template.render(context, request))

def detail(request, landmark_id):
    '''
    Returns template
    '''
    try:
        landmark = Landmark.objects.get(id = landmark_id)
    except Landmark.DoesNotExist:
        raise Http404("landmark does not exist")

    template = loader.get_template('quiz/detail.html')
    context = {
        'landmark': landmark,
    }
    return HttpResponse(template.render(context, request))

def results(request, landmark_id):
    try:
        landmark = Landmark.objects.get(id = landmark_id)
    except Landmark.DoesNotExist:
        raise Http404("landmark does not exist")

    template = loader.get_template('quiz/results.html')
    context = {
        'landmark': landmark,
    }
    return HttpResponse(template.render(context, request))

def vote(request, landmark_id):
    #check Q exists
    try:
        landmark = Landmark.objects.get(id = landmark_id)
    except Landmark.DoesNotExist:
        raise Http404("landmark does not exist")
    #check choice chosen exists
    try: 
        choice = landmark.choice_set.get(id = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):  #revert to Landmark page
        template = loader.get_template('quiz/detail.html')
        context = {
        'landmark': landmark,
        'error_message': "You didn't select a choice!",
        }
        return HttpResponse(template.render(context, request))
    else: #change the guess to true
        for c in landmark.choice_set.all():
            c.guess = False
            c.save()
        choice.guess = True
        choice.save()
        

        url = reverse('results', args = (landmark_id,) )  #goes to results url of the correct Landmark.
        return HttpResponseRedirect(url)