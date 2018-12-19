# Django CDNJS

Django CDNJS is the small template tag, that allows you to load external cdn
resources by name. You can download any required CDN as well as use only CDN's
URL by disabling/enabling resource downloading.

# How it works

Website https://cdnjs.com has an [API](https://cdnjs.com/api) for all cdn 
repositories stored at database. This API was used in `django-cdnjs`.

# Installation

Install pip-package

    pip install django-cdnjs

Add `cdnjs` to your installed apps:

    INSTALLED_APPS = (
        ...
        'cdnjs',
    )
    
    # Configure settings
    CDNJS_STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'cdn')
    CDNJS_STATIC_URL = '/static/cdn/' # With "/" at end of string

# Usage example

If you will not provide filename from repository, which url you need, 
django-cdnjs will return default repository file. For example `font-awesome` 
default file is `css/font-awesome.min.css`

Same for version - django-cdnjs will load latest available version and **not
always stable**

**default-files.html**

    {% load cdnjstag %}
    
    <!DOCTYPE html>
    ...
    
    <link rel="stylesheet" href="{% cdn "font-awesome" %}">
    <script type="text/javascript" src="{% cdn "jquery" %}"></script>
    ...
    
Usually you can specify which version you need to be loaded. Just add slash 
after repository name and specify version. Example:
    
**specify-version.html**

    {% load cdnjstag %}
    
    <!DOCTYPE html>
    ...
    
    <link rel="stylesheet" href="{% cdn "font-awesome/4.7.0" %}">
    <script type="text/javascript" src="{% cdn "jquery/3.2.1" %}"></script>
    ...
    
Second optional argument of `cdn` tag is the file which should be selected to
build cdn-url or local-uri. For example, repository of the `boostrap` css 
framework has css-files as well as js. CDNJS provides js-file as the default,
so we need to specify manually which file do we need.
    
**specify-file.html**

    {% load cdnjstag %}
    
    <!DOCTYPE html>
    ...
    
    <link rel="stylesheet" href="{% cdn "bootstrap/3.3.7" "bootstrap.min.css" %}">
    <script type="text/javascript" src="{% cdn "jquery/3.2.1" %}"></script>
    <script type="text/javascript" src="{% cdn "bootstrap/3.3.7" "bootstrap.min.js" %}"></script>
    ...
    
And here you can see that I had some typo in repository name. But `cdnjs` API 
returns results by query term `bootstrap` and `twitter-bootstrap` is the first
of them. So you can make typos.

If you want use CDNJS with [django-assets](https://django-assets.readthedocs.io/en/latest/):

**specify-file.py**

    from django_assets import Bundle, register
    from cdnjs import CDNStorage
    
    cdnjs_manager = CDNStorage()
    
    css = Bundle(
        cdnjs_manager.get(font-awesome),
        cdnjs_manager.get('mini.css'),
        filters='jsmin',
        output='css/app.css'
    )

    register('css_all', css)

**specify-file.html**

    {% load assets %}

    {% assets "css_all" %}
        <link rel="stylesheet" type="text/style" href="{{ ASSET_URL }}"/>
    {% endassets %}
    

Here, django-assets take libraries generates with django-cdnjs and package this in one file.
Finally, include the bundle you defined in the appropriate place within your templates.
 
# Configuration

### Required options

Anyway, you should provide two django settings module properties

    # This property uses not only for storing remote repositories,
    # but for cdn urls cache too. So this option is required. 
    CDNJS_STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'cdn')
        
    # This option is required, because I don't now why. You should
    # know that it's so. Even if you using FORCE_CDN.
    # If you want, you can contribute it and fix. =)
    CDNJS_STATIC_URL = '/static/cdn/' # With "/" at end of string
    

### Do not load remote repository

By default `cdnjs` downloads remote repository to be used without accessing 
remote resources.

    # If you need to use only local urli without CDN loading,
    # just set this option to True
    CDNJS_USE_LOCAL = True
     
    # True - download remote repository and use local URI
    # False - (default) do not download remote repository and use CDN URI
    
    
### Settings

|Option|Default|Required|Comment|
|---|---|---|---|
|CDNJS_STATIC_ROOT|None|True|Absolute path to the cdn static root.|
|CDNJS_STATIC_URL|None|True|Absolute path to the cdn static url.|
|CDNJS_USE_LOCAL|False|False|Should tag download requested repository and use local URI instead of CDN URI.|
