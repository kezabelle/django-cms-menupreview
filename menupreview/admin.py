from copy import copy
from functools import update_wrapper
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from menus.models import CacheKey
from cms.models.pagemodel import Page
from menupreview.models import MenuPreview
from menupreview.forms import (MenuPreviewForm, SubmenuPreviewForm,
    MenuBelowIdPreviewForm)

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
            url(regex=r'^cache_keys/$',
                view=self.cache_keys,
                name='%s_%s_cache_keys' % (self.model._meta.app_label,
                    self.model._meta.module_name)
            ),
            url(regex=r'^$',
                view=self.index,
                name='%s_%s_changelist' % (self.model._meta.app_label,
                    self.model._meta.module_name)
            ),
            url(regex=r'^show_menu/$',
                view=self.show_menu,
                name='%s_%s_menu' % (self.model._meta.app_label,
                    self.model._meta.module_name)
            ),
            url(regex=r'^show_sub_menu/$',
                view=self.show_sub_menu,
                name='%s_%s_sub_menu' % (self.model._meta.app_label,
                    self.model._meta.module_name)
            ),
            url(regex=r'^show_menu_below_id/$',
                view=self.show_menu_below_id,
                name='%s_%s_menu_below_id' % (self.model._meta.app_label,
                    self.model._meta.module_name)
            ),


        )
    urls = property(urls)

    def index(self, request):
        return render_to_response('admin/menupreview/index.html',
            {'app_label': self.model._meta.app_label, 'opts': self.opts,
            'using_reverse_ids': Page.objects.filter(reverse_id__isnull=False).exists(),
            'title': _('Menu preview administration')},
            context_instance=RequestContext(request))
 
    def cache_keys(self, request):
       return render_to_response('admin/menupreview/cache_keys.html',
            {'app_label': self.model._meta.app_label, 'opts': self.opts,
            'title': _('Cache keys'), 'object_list': CacheKey.objects.all()},
            context_instance=RequestContext(request))
 
    def all_menus(self, request, template, subtemplate, form_class, title):
        form = form_class(request, data=request.GET or None, files=None)
        if request.is_ajax():
            template = subtemplate #'_ajax.'.join(subtemplate.rsplit('.', 1))

        # oh my word. turns out request.path, at least, is mutable (but POST/GET
        # aren't?! Even so, we'll take a copy and modify it.
        if form.is_valid():
            request = copy(request)
            request.path = form.cleaned_data.get('active_page', request.path)
        ctx = {
            'form': form,
            'app_label': self.model._meta.app_label,
            'opts': self.opts,
            'title': _(title),
            'subtemplate': subtemplate,
        }
        return render_to_response(template, ctx,
            context_instance=RequestContext(request))
  
    def show_menu(self, request):
        return self.all_menus(request, 'admin/menupreview/form.html',
            'admin/menupreview/menupreview_ajax.html', MenuPreviewForm,
            'Full menu preview')

    def show_sub_menu(self, request):
        return self.all_menus(request, 'admin/menupreview/form.html',
            'admin/menupreview/submenupreview_ajax.html', SubmenuPreviewForm,
            'Sub menu preview')

    def show_menu_below_id(self, request):
        return self.all_menus(request, 'admin/menupreview/form.html',
            'admin/menupreview/menubelowidpreview_ajax.html', MenuBelowIdPreviewForm,
            'Menu below ID preview')
admin.site.register(MenuPreview, FakeModelAdmin)

