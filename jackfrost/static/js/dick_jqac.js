/**
 * Created by PyCharm.
 * User: Usuario
 * Date: 8/10/12
 * Time: 23:33
 * To change this template use File | Settings | File Templates.
 */

var __JQACCanCallEvent = function(wrapper, event)
{
    return (wrapper.length > 0 && (typeof event == 'function'));
};

var __JQACSelect_set_event = function(wrapper, event, item)
{
    if (__JQACCanCallEvent(wrapper, event))
    {
        return event(wrapper[0], item.key, item);
    }
    return true;
};

var __JQACSelect_del_event = function(wrapper, event)
{
    if (__JQACCanCallEvent(wrapper, event))
    {
        return event(wrapper[0], wrapper.val());
    }
    return true;
};

var __JQACSelect_setvalue = function(item, wrapper_text, wrapper_hidden, handler_before, handler_after) {
    if (!__JQACSelect_set_event(wrapper_hidden, handler_before, item)) return;
    wrapper_hidden.val(item.key);
    wrapper_text.addClass('ac-item-selected').prop("readonly", true).val(item.label);
    __JQACSelect_set_event(wrapper_hidden, handler_after, item);
};

var __JQACSelect_delvalue = function(wrapper_text, wrapper_hidden, handler_before, handler_after) {
    if (!__JQACSelect_del_event(wrapper_hidden, handler_before)) return;
    wrapper_hidden.val('');
    wrapper_text.removeClass('ac-item-selected').prop("readonly", false).val('');
    __JQACSelect_del_event(wrapper_hidden, handler_after);
};

var __JQACSelectMultiple_values = {};

var __JQACSelectMultiple_get_value = function(hidden_id) {
    if (!(hidden_id in __JQACSelectMultiple_values)) {
        __JQACSelectMultiple_values[hidden_id] = [];
    }
    return __JQACSelectMultiple_values[hidden_id];
};

var __JQACSelect_add_event = function(wrapper, wrapper_list, event, item)
{
    if (__JQACCanCallEvent(wrapper, event))
    {
        return event(wrapper[0], wrapper_list[0], item.key, item);
    }
    return true;
};

var __JQACSelect_rem_event = function(wrapper, wrapper_list, event, pos)
{
    if (__JQACCanCallEvent(wrapper, event))
    {
        var elements = __JQACSelectMultiple_get_value(wrapper.attr('id'));
        return event(wrapper[0], wrapper_list[0], elements[pos], pos);
    }
    return true;
};

var __JQACSelectMultiple_addvalue = function(item, wrapper_list, wrapper_text, wrapper_hidden, handler_before, handler_after) {
    if (!__JQACSelect_add_event(wrapper_hidden, wrapper_list, handler_before, item)) return;
    var values = __JQACSelectMultiple_get_value(wrapper_hidden.attr('id'));
    wrapper_text.val('');
    values.push(item.key);
    wrapper_hidden.val(JSON.stringify(values));
    wrapper_list.append($('<option></option>').attr('value', item.key).text(item.label));
    __JQACSelect_set_event(wrapper_hidden, wrapper_list, handler_after, item);
};

var __JQACSelectMultiple_remvalue = function(pos_array, wrapper_list, wrapper_hidden, handler_before, handler_after) {
    if (!__JQACSelect_rem_event(wrapper_hidden, wrapper_list, handler_before, pos_array)) return;
    var values = __JQACSelectMultiple_get_value(wrapper_hidden.attr('id'));
    values.splice(pos, 1);
    wrapper_hidden.val(JSON.stringify(values));
    wrapper_list.children("option:selected").remove();
    __JQACSelect_del_event(wrapper_hidden, wrapper_list, handler_after, pos_array);
};

var JQACTextInput = function($, id, source){
    $(function(){
        $("#" + id).autocomplete({
            source: source
        });
    });
};

var JQACSelect = function($,
                          id,
                          autocomplete_source_url,
                          initialdata_source_url,
                          initialdata,
                          before_set,
                          after_set,
                          before_del,
                          after_del) {

    var selector_hidden = '#' + id;
    var selector_text = selector_hidden + '-text';
    var wrapper_hidden = $(selector_hidden);
    var wrapper_text = $(selector_text);

    var hasvalue = function()
    {
        return wrapper_hidden.val() != '' || wrapper_text.hasClass('ac-item-selected') || wrapper_text.prop('readonly');
    };

    $(function(){
        wrapper_text.autocomplete({
            source: autocomplete_source_url,
            select: function(e, ui){
                __JQACSelect_setvalue(ui.item, wrapper_text, wrapper_hidden, before_set, after_set);
            }
        });

        wrapper_text.keydown(function(e){
            if (e.which == 46 && hasvalue()) __JQACSelect_delvalue(wrapper_text, wrapper_hidden, before_del, after_del);
        });

        if (initialdata != null)
        {
            var params = {value: initialdata};
            var callback = function(data){
                __JQACSelect_setvalue(data, wrapper_text, wrapper_hidden, before_set, after_set);
            };
            $.get(initialdata_source_url, params, callback, 'json');
        }
    });
};

var JQACSelectMultiple = function($,
                                  id,
                                  autocomplete_source_url,
                                  initialdata_source_url,
                                  initialdata,
                                  before_add,
                                  after_add,
                                  before_del,
                                  after_del){

    var selector_hidden = '#' + id;
    var selector_text = selector_hidden + '-text';
    var selector_list = selector_hidden + '-list';
    var wrapper_hidden = $(selector_hidden);
    var wrapper_text = $(selector_text);
    var wrapper_list = $(selector_list);

    $(function(){
        wrapper_text.autocomplete({
            source: autocomplete_source_url,
            select: function(e, ui) {
                __JQACSelectMultiple_addvalue(ui.item, wrapper_list, wrapper_text, wrapper_hidden, before_add, after_add);
            }
        });

        wrapper_list.keydown(function(e){
            var items = wrapper_list.children();
            var positions = [];
            items.each(function(i, e) {
                if ($(e).is(":selected")) positions.push(i);
            });
            if (e.which == 46 && positions.length > 0) __JQACSelect_delvalue(wrapper_text, wrapper_hidden, before_del, after_del);
        });

        if (initialdata != null)
        {
            var params = {value: initialdata};
            var callback = function(data){
                var x;
                $.each(data, function(i, item){
                    __JQACSelectMultiple_addvalue(item, wrapper_list, wrapper_text, wrapper_hidden, before_add, after_add);
                });
            };
            $.post(initialdata_source_url, params, callback, 'json');
        }
    });
};