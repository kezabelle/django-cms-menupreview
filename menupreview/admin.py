from copy import copy
from functools import update_wrapper
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from menupreview.models import MenuPreview
from menupreview.forms import MenuPreviewForm

class FakeModelAdmin(object):
    fields = None
    fieldsets = None
    exclude = None
    date_hierarchy = None
    ordering = None
    list_select_related = False
    save_as = False
    save_on_top = False

    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site

    def get_model_perms(self, request):
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request)
        }

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def urls(self):
        from django.conf.urls.defaults import patterns, url
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        return patterns('',
            url(regex=r'^$',
                view=self.changelist_view,
                name='%s_%s_changelist' % (self.model._meta.app_label,
                    self.model._meta.module_name)
            )
        )
    urls = property(urls)

    def changelist_view(self, request, template_name='admin/menupreview/menupreview.html'):
        form = MenuPreviewForm(request, data=request.GET or None, files=None)
        if request.is_ajax():
            template_name = '_ajax.'.join(template_name.rsplit('.', 1))

        # oh my word. turns out request.path, at least, is mutable (but POST/GET
        # aren't?! Even so, we'll take a copy and modify it.
        if form.is_valid():
            request = copy(request)
            request.path = form.cleaned_data.get('active_page', request.path)

        ctx = {
            'form': form,
            'app_label': self.model._meta.app_label,
            'opts': self.opts,
            'title': _('Menu preview'),
        }
        return render_to_response(template_name, ctx,
            context_instance=RequestContext(request))
admin.site.register(MenuPreview, FakeModelAdmin)

