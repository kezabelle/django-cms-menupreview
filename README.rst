============
Menu Preview
============

Rationale
=========

Because no-one can easily visualise what parameters will do to a  `django CMS <http://www.django-cms.org>`_ site using ``{% show_menu %}``

Usage
=====

Add ``'menupreview'`` to your ``INSTALLED_APPS``, and visit the  `Django <http://www.djangoproject.com>`_ administration.

.. _implementation:

Implementation
==============

It's a complete hack. Here, let's count the ways:

1. It uses a standard Model object, which has no attributes, and declares itself as unmanaged by the ORM.
2. The model declares its ``app_label`` as **cms**. Yes, really. Because I wanted it grouped with the rest of the CMS functionality.
3. It has an empty migration for `South <http://south.aeracode.org/>`_, just for safety's sake.
4. It uses a standard python class (rather than a ModelAdmin instance) to register itself to the Django administration, and simply provides enough attribute defaults to trick the admin validation.
5. The admin class overrides permissions management to only display the hackyness to super users, which is a small mercy.
6. It overrides the usual URLs, and provides its own changelist, which is really anything but.
7. The changelist, awesomely, **modifies the request object** by changing the ``path`` attribute, to trick ``{% show_menu %}`` into thinking the right node is selected. I am genuinely surprised that the object isn't immutable.
8. It depends on the new, *easy* way to get data from a form instance in Django 1.3, where ``form.field.value`` can return initial or bound data. I could probably fix this to support 1.2, though.
9. It uses AJAX, but doesn't do so in a particularly nice way, subsequently, form validation messages are pretty much out the window. Though it does re-use the provided version of jQuery, and cleans up after itself by being anonymous.

On the up side of all of that, it should be a fair emulation of the menu you'd otherwise be experimenting with in templates, including any registered ``Menu`` or ``AttachMenu`` instances. And it should technically work without AJAX, which is always a bonus.

Dependencies
============

* `Django <http://www.djangoproject.com>`_ 1.3+
* `django CMS <http://www.django-cms.org>`_ 2.2+
    * It might work on 2.1.3, but I've not yet tried.

Contributing
============

Presumably, if you're reading this bit, you have a problem with it. Or you just want there to be less numbers in the implementation_ section.
Check `my GitHub <https://github.com/kezabelle>`_, which is probably where this project is.

Development status
==================

At the moment, there isn't any.
