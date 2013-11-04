from django.core.urlresolvers import resolve, reverse
from django.shortcuts import redirect
from django.utils.decorators import available_attrs

from functools import wraps
from operator import itemgetter
from urlparse import urlparse

import uuid


__all__ = ['Wizard', 'wizard_check_id', 'wizard_check_data']


def wizard_check_id(redirect_to='/'):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if not 'wizard_id' in request.session:
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def wizard_check_data(keys=None, redirect_to='/'):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            if not 'form_data' in request.session:
                return redirect(redirect_to)
            else:
                data = request.session['form_data']

                if keys is not None and not all(k in data for k in keys):
                    return redirect(redirect_to)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


class Wizard(object):

    def __init__(self, request, steps_data):
        self.request = request
        self.data = request.session.get('form_data', {})
        self.user = request.user
        self.current_step = None
        self.steps = self.__get_steps(steps_data)
        self.id = None

        self.__resolve_initial_state()

    def __get_id(self):
        if 'wizard_id' not in self.request.session:
            self.request.session['wizard_id'] = uuid.uuid4().hex

        return self.request.session['wizard_id']

    def __resolve_initial_state(self):
        urls = map(itemgetter('url'), self.steps)
        ref_path = urlparse(self.request.META.get('HTTP_REFERER', '')).path
        current_step = self.current_step

        if current_step is None or (current_step['index'] == 0 and ref_path not in urls):
            self.cleanup()

        self.id = self.__get_id()

    def __get_steps(self, steps_data):
        steps = []
        index = 0

        for item in steps_data:
            anonymous_required = item.get('anonymous_required', False)
            
            if anonymous_required and not self.user.is_anonymous():
                continue
            else:
                resolved = resolve(self.request.path)
                is_current = resolved.url_name == item['url_name']

                item_copy = item.copy()
                item_copy.update({
                    'index': index,
                    'is_current': is_current
                })

                if is_current:
                    self.current_step = item_copy

                steps.append(item_copy)
                index += 1

        for step in steps:
            step.update({'url': reverse(step['url_name'], args=step.get('url_params', []))})

            if step['index'] < self.current_step['index']:
                step.update({'passed': True})

            if step['is_current']:
                prev_url = None

                if step['index'] > 0:
                    prev_url = steps[steps.index(step) - 1]['url']

                step.update({'prev': prev_url})

        return steps

    def set_data(self, forms):
        modified = False

        if self.data:
            for k, v in self.request.POST.iteritems():
                self.request.session['form_data']['post'][k] = v
            modified = True
        else:
            self.request.session['form_data'] = {'post': self.request.POST.copy()}

        for key in forms:
            self.request.session['form_data'][key] = forms[key].cleaned_data

        if modified:
            self.request.session.modified = True

        self.data = self.request.session['form_data']

        return None

    def cleanup(self):
        for key in ('form_data', 'wizard_id'):
            if key in self.request.session:
                del self.request.session[key]

        self.data = {}
