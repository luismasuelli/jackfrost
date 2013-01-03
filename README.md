=========
jackfrost
=========

J.A.C.K.F.R.O.S.T. (Jquery Auto Complete Kit For Remote Object Safe Targeting)
is an autocomplete technology based on the jquery ui plugin which allows the
search and pick of remote objects (i.e. stored model objects) from the front
end as a field value, supporting any dataset/query and having that object at
the server side.

==========
Installing
==========

Put the application package named jackfrost in your project.
In settings.py:
* Install the application.
* Customize the jQuery library (static files) in these variables:
  * JACKFROST_JQUERY_LIB : path to the jquery library.
  * JACKFROST_JQUERYUI_LIB : path to the jquery-ui library.
  * JACKFROST_JQUERYUI_CSS : path to the theme to use by the application.
  (Note: the application ships with a version of jquery, jqueryui, and a theme.
   If one or more of these settings are not specified, their shipped defaults
   will be used instead).
* Add the middleware jackfrost.middlewares.AutocompleteMiddleware to the
  middlewares tuple.

=====
Using
=====

This application was meant to provide alternatives to the ModelChoiceField and
ModelMultipleChoiceField components by allowing real-time AJAX searches from the
client side. Three form fields are provided and meant to use for simple foreign
keys or many-to-many relationships.

In the model declarations:
* Declare your models as usual.

In the views declarations you will declare "channels" or "lookups". This is the
most important thing since these channels will be used for every ajax request
performed by the component. Channels are not themselves views/callables, but
objects which contain views for the needed ajax calls, so you must declare your
channels and then import them for their urls.
* Declaring a channel:
  * In module jackfrost.lookups a function named "register" is used to create them.
    parameters (ordered by position, with the exact name):
        pattern: The url pattern you would use to declare it as a normal view.
          this pattern must contain a single "%s" format marker because it will
          be used to create three urls: each one replacing the %s for "many",
          "one", and "ac" (respectively: M2M initialization, FK initialization,
          and autocomplete search). e.g. r'/foo/bar/%s/' or r'/foo/mychannel-%s/'
        name: The name to perform an url reversal. for each generated url, a
          name will be generated from this name by concatenating "-many", "-one"
          and "ac" respectively. The name is both used to register the channel
          object and to obtain it back.
        queryset: A query to search the items from, and validate the items against.
          The query MUST be the same as (or a subset of) the source for the
          ForeignKey or ManyToMany for which it's intended. IMPORTANT: for that
          model class, __unicode__(self) must be defined since it will be the
          caption for the autocomplete results, selection, and initialization.
        filter (optional): None or a callable as follows:
          expected parameters (by position):
            query: the query specified in queryset parameter.
            request: the current WSGIRequest object (it will be an AJAX request).
          expected return value:
            a queryset obtained from the query parameter, e.g., by taking into
            account current request details like user, site, or session and applying
            filters to it.
          remarks: specifying None instead of a callable does not perform any
            filtering (the queryset is not modified/filtered).
        field_list: A sequence of fields in the query to perform the search against.
          For every search term, a LIKE comparison is performed against each field
          in this list. e.g. passing ('name', 'description') will list every item
          having at least one search term in any part of those fields contents.
          THOSE FIELDS MUST BE VARCHAR OR TEXT FIELDS.
        limit (optional): A positive integer specifying the max amount of results to
          retrieve for the autocomplete jQuery plugin. Defaults to 15
        to_field_name (optional): The field, in the target model class, to validate
          against when objects are validated or initialized. It should be a primary
          or unique key. Otherwise there's a big chance that validation errors
          occur or keys be initialized to an unintended model instance. It defaults
          to "pk" (the alias for every model to the model-specific pk field).
        throw403_if (optional): None or a callable as follows:
          expected parameters (by position):
            request: the current (AJAX) request.
            context: "ac" (if it's the channel's autocomplete url)
                     "one" (for the ForeignKey initialization url)
                     "many" (for the ManyToMany initialization url)
          expected return value:
            a value evaluable to True will cause the current AJAX call to
            fail with a 403 (forbidden) HTTP error. a value evaluable to
            False will not.
          remarks: specifying None will not perform this check-and-error.
        throw404_if (optional): None or a callable like throw403_if except
          that the raised error response will be 404 (Not Found) instead of
          403 (Forbidden).
        extra_data_getter (optional): None or a callable as follows:
          expected parameters (by position):
            instance: an instance fetched by the queryset or filtered queryset.
          expected return value:
            a JSON-serializable value representing some extra data needed in
            the client side (perhaps used by a custom render in the jQuery ui
            component).
          remarks: specifying None will cause the extra data to be a void object
            (i.e. an empty dict in python and an empty object in javascript).
  * After registering it, it must be referenced by it's urls.
    In module jackfrost.lookups a variable named registered_lookups will reference
      a dictionary containing the current lookup by it's name (2nd parameter
      specified in the lookup register() call). it's url pack must be gotten.
      e.g. an urls.py file (usually, you will put these crap in those urls.py files):

      ##################### start of file
      #put this import among the other needed imports
      from jackfrost import lookups

      #... more stuff here you would need

      #sample call with no optional parameters
      lookups.register(r'/channels/first-%s/', 'myFirstChannel', MyModel.objects.all())

      #... more stuff here you would need

      url_patterns = patterns('',) + lookups.registered_lookups['myFirstChannel'].urls
      #you can add (+) as many channels as you want because the .urls property returns
      #a tuple with the 3 generated urls. in this case just one channel is added to
      #the original urls (you can add other urls to the patterns call but watch out
      #for name collisions).
      ##################### end of file

In the forms declarations:
* Import the needed fields from jackfrost.fields module:
  * AutocompleteCharField (an improved CharField with autocomplete in CharField)
  * AutocompleteModelChoiceField (replaces ModelChoiceField in ForeignKey)
  * AutocompleteModelMultipleChoiceField (replaces ModelMultipleChoiceField in ManyToMany)
  (You cannot, and you should not, change the widgets).
  (They can take more **kwargs params, the same as the fields they replace).

* Declare your ModelForm and override their fields as follows:
For each field you want to convert to it's autocomplete version, just override it
by declaring it as a new file (matching the model field name) as explained in the
last paragraph (which AutocompleteField is intended for which Model field or
non-AutoComplete form field). Overriding is as follows:
  #referencing the declared channel
  myCharField = AutocompleteCharField('myChannel')
  #referencing the declared channel (or perhaps another channel. it doesn't matter
  #as long as it's declared as described). widget_attrs contains parameters that
  #will be explained later.
  myForeignKeyField = AutocompleteModelChoiceField('myChannel' [, widget_attrs])
  #referencing another declared channel (or perhaps the same...). widget_attrs
  #contains parameters that will be explained later.
  myManyToManyField = AutocompleteModelMultipleChoiceField('test_app.languages' [, widget_attrs])
  #REMEMBER THAT IN THE FOREIGN KEY AND MANY-TO-MANY FIELDS THERE'S A HIDDEN
  #INPUT THAT CONTAINS THE REAL ID AND VALUE TO SEND TO THE SERVER.

In the template
* Including media in the template:
DON'T FORGET TO INCLUDE THE form.media REFERENCE IN THE TEMPLATE OR ELSE THESE
COMPONENTS WILL NOT WORK (these would happen with every django components app -.-'').

===========
Customizing
===========

The components can be customized in several ways.

* The extra_data_getter can be used to bring more data about the instance
  (it would be used to custom-render or consider at events).
* For AutocompleteModelChoiceField component, widget_attrs may be specified
  containing expressions returning javascript event handlers (i.e. callback
  functions) whose signatures are:
  * Element assignment event:
    * before_set: A function with signature function(Event, key, object).
      If it returns false, the element is not set.
      Can safely have no return statement.
    * after_set: A function with the same signature that before_set.
      The return value is not taken into account.
  * Element deletion event:
    * before_del: A function with signature function(Event, key).
      If it returns false, the element is not deleted.
      Can safely have no return statement.
    * after_del: A function with the same signature that before_del.
      The return value is not taken into account.
  * renderer: A function with signature function(event, key, object).
      It must return an HTML string that will be the content for
      the rendered element. By not returning any value, the default jquery-ui
      rendering will be applied.
  (These events may be alternatively set in client-side by binding to the hidden
   input these functions in events beforeSet, afterSet, beforeDelete, afterDelete,
   and render).
* For AutocompleteModelMultipleChoiceField component, widget_attrs may be specified
  containing expressions returning javascript event handlers (i.e. callback
  functions) whose signatures are:
  * Element addition event (before and after):
    * before_set: A function with signature function(Event, key, object).
      If it returns false, the element is not added.
      Can safely have no return statement.
    * after_set: A function with the same signature that before_add.
      The return value is not taken into account.
  * Element removal event (before and after):
    * before_rem: A function with signature function(Event, listbox, key, position).
      If it returns false, the element is not removed.
      Can safely have no return statement.
    * after_rem: A function with the same signature that before_rem.
      The return value is not taken into account.
  * renderer: A function with signature function(event, key, object).
      It must return an HTML string that will be the content for
      the rendered element. By not returning any value, the default jquery-ui
      rendering will be applied.
  (These events may be alternatively set in client-side by binding to the hidden
   input these functions in events beforeAdd, afterAdd, beforeRemove, afterRemove,
   and render).

("Event" is a jquery Event.
 "key" is the object field value.
 "object" is a javascript literal object containing the fields:
   * value = label = the model object's caption
   * key = the key parameter
   * extra = the data as generated by the extra_data_getter if specified
 "listbox" is the HTML5 DOM Select component (rendered by the browser) to store
   the elements.
 "position" is the position of the key in the listbox to be removed).

===================
Future Improvements
===================

* Customizing AJAX error handling (a new event).
* Customizing the model object caption in a per-channel way and not just the model's
  __unicode__ method (keeping it as the default option).
* Initialization events for the components (distinguishing them from the set/add
  events).
* Caching/multisourcing.

===========
Limitations
===========

The ManyToMany relationship to use with this AutocompleteModelMultipleChoiceField
must NOT have a "through" parameter set.

Other known limitations are explained in the Future Improvements section.

============
Contact info
============

You can contact me for bugs, suggestions and doubts to malavon_despana@hotmail.com.
Please put in the subject "jackfrost django app" so I can distinguish that mail
from the bulk i usually delete.