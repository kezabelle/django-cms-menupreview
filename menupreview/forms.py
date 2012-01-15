from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from menus.menu_pool import menu_pool
from cms.models.pagemodel import Page

level_opts = [(x, x) for x in xrange(0, 21)]

class MenuPreviewForm(forms.Form):
    start_level = forms.TypedChoiceField(label=_('Starting from level'), initial=0, choices=level_opts, coerce=int)
    end_level = forms.TypedChoiceField(label=_('Ending at level'), initial=20, choices=level_opts, coerce=int)
    extra_inactive = forms.TypedChoiceField(label=_('Extra inactive'), initial=20, choices=level_opts, coerce=int)
    extra_active = forms.TypedChoiceField(label=_('Extra active'), initial=20, choices=level_opts, coerce=int)
    active_page = forms.ChoiceField(label=_('Selected page'), initial='/')

    def __init__(self, request, *args, **kwargs):
        super(MenuPreviewForm, self).__init__(*args, **kwargs)
        self.fields['active_page'].choices = [(n.get_absolute_url(), mark_safe(u'%s%s' % ('&nbsp;&nbsp;'* n.level, n.title)))
            for n in menu_pool.get_nodes(request)]

    def clean(self):
        cd = self.cleaned_data
        if cd.get('start_level', 0) > cd.get('end_level', 0):
            raise forms.ValidationError('boo hiss')
        return cd


class SubmenuPreviewForm(forms.Form):
    end_level = forms.TypedChoiceField(label=_('Ending at level'), initial=20, choices=level_opts, coerce=int)
    active_page = forms.ChoiceField(label=_('Selected page'), initial='/')

    def __init__(self, request, *args, **kwargs):
        super(SubmenuPreviewForm, self).__init__(*args, **kwargs)
        self.fields['active_page'].choices = [(n.get_absolute_url(), mark_safe(u'%s%s' % ('&nbsp;&nbsp;'* n.level, n.title)))
            for n in menu_pool.get_nodes(request)]


class MenuBelowIdPreviewForm(forms.Form):
    start_level = forms.TypedChoiceField(label=_('Starting from level'), initial=0, choices=level_opts, coerce=int)
    end_level = forms.TypedChoiceField(label=_('Ending at level'), initial=20, choices=level_opts, coerce=int)
    extra_inactive = forms.TypedChoiceField(label=_('Extra inactive'), initial=20, choices=level_opts, coerce=int)
    extra_active = forms.TypedChoiceField(label=_('Extra active'), initial=20, choices=level_opts, coerce=int)
    active_page = forms.ChoiceField(label=_('Selected page'), help_text=_('Only pages with a reverse ID are available'))

    def __init__(self, request, *args, **kwargs):
        super(MenuBelowIdPreviewForm, self).__init__(*args, **kwargs)
        self.fields['active_page'].choices = [(p.reverse_id, p.get_menu_title())
            for p in Page.objects.filter(reverse_id__isnull=False)]

    def clean(self):
        cd = self.cleaned_data
        if cd.get('start_level', 0) > cd.get('end_level', 0):
            raise forms.ValidationError('boo hiss')
        return cd

