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
 
# Configuration

### Required options

Anyway, you should provide two django settings module properties

    # This property uses not only for storing remote repositories,
    # but for cdn urls cache too. So this option is required. 
    CDN_STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'cdn')
        
    # This option is required, because I don't now why. You should
    # know that it's so. Even if you using FORCE_CDN.
    # If you want, you can contribute it and fix. =)
    CDN_STATIC_URL = '/static/cdn/' # With "/" at end of string
    

### Do not load remote repository

By default `cdnjs` downloads remote repository to be used without accessing 
remote resources.

    # If you need to use only cdn urls without repository downloading,
    # just set this option to True
    FORCE_CDN = True
     
    # True - do not download remote repository
    # False - (default) download remote repository
