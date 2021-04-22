## 2.1.3
**FIXED**
* Fixed double querying for list API

## 2.1.2
**ADDED**
* get_api_queryset class method on the model mixin. So, be available on the models 
* Deprecated "queryset" on exposed_api class method.

## 2.1.1
**ADDED**
* Added test cases for test app
* App directory structure has changed. But, no external effect.

**BUG FIXED**
* Import error and some other minor fixes

## 2.1.0
**ADDED**
* Added support for Django's prefetch and select related.

## 2.0.0
**ADDED**
* Dynamic API filtering with model fields.
* Support all the django filter on API params. Like: ?search=1&title:icontains=test

**UPDATED**
* Settings config data type updated with default configuration

## 1.0.10
**ADDED**
* Added Dockerfile and compose file for local dependency

**BUG FIXED**
* Django REST Framework six dependent version upgraded

**UPDATED**
* Updated API prefix and doc

## 1.0.8
**ADDED**
* API Multiple Version

## 1.0.7
**BUG FIXED**
* Fixed paginated queryset returning issue

## 1.0.6
**UPDATED**
* Django version updated due to stop vulnerability warning

**ADDED**
* Create from two level of json according to API format

**BUG FIXED**
* Fixed permission class empty issue while user is not giving
* Fixed Serializer list api data property calling issue


## 1.0.5
**UPDATED**
* Django version updated due to stop vulnerability warning

## 1.0.4
**ADDED**
* Nothing

**UPDATED**
* Nothing

**BUG FIXED**
* HTTP verb conflicting issue
* Proper http handling

## 1.0.3
**ADDED**
* Details API [PUT, PATCH, DELETE]
* Allowed method choosing option
* Only view class or only serializer class can override
* Added support for view class or viewset or generic view

**UPDATED**
* Nothing

**BUG FIXED**
* Fixed queryset override issue
* Fixed queryset caching issue


## 0.1.2
**ADDED**
* Nothing

**UPDATED**
* Nothing

**BUG FIXED**
* pip install failed issue
* twine upload issue

## 0.1.1
**ADDED**
* Added utility classes for support 
* Added example app for local testing(Not added in package)

**UPDATED**
* Updated directory structure of app
* Seperated mixins

**BUG FIXED**
* Fixed wrong queryset bug
* Added loop iteration improvements

## 0.0.1
**ADDED**
* Model Based api writing
* Ability to override Serializer, View class, queryset
* Work on proxy model

**BUG FIXED**
* Nothing as it's initial release
