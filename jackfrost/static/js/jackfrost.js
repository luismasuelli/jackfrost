/**
 *
 * General stuff
 * * event handlers
 *
 */

/**
 *
 * Event handlers
 *
 */

function __jackfrost_autocomplete_on_render(wrapper, ul, item) {
    var return_value = wrapper.triggerHandler('render', [ul, item]);
    return (typeof return_value == 'undefined') ? item.label : return_value;
}

/**
 *
 * Internal calls
 *
 */

function __jackfrost_autocomplete_render(wrapper_hidden, ul, item) {
    return $( "<li></li>" )
        .data( "item.autocomplete", item )
        .append( "<a>" + __jackfrost_autocomplete_on_render(wrapper_hidden, ul, item) + "</a>" )
        .appendTo( ul );
}

/**
 *
 * General stuff end
 *
 */

/**
 *
 * JackFrost Input stuff (it's just a textbox with jquery ui Auto Complete)
 * * constructor
 *
 */

/**
 *
 * Constructor
 *
 */

function jackfrost_input($, id, source){
    $(function(){
        $("#" + id).autocomplete({
            source: source
        });
    });
}

/**
 *
 * JackFrost Input stuff end
 *
 */

/**
 *
 * JackFrost Singlechoice stuff
 * * event handlers
 * * internal calls
 * * constructor
 *
 **/

/**
 *
 * Event handlers
 *
 */

function __jackfrost_singlechoice_before_set(wrapper, item) {
    var return_value = wrapper.triggerHandler('beforeSet', [item.key, item]);
    return (typeof return_value == 'undefined') || return_value;
}

function __jackfrost_singlechoice_after_set(wrapper, item) {
    var return_value = wrapper.triggerHandler('afterSet', [item.key, item]);
    return (typeof return_value == 'undefined') || return_value;
}

function __jackfrost_singlechoice_before_del(wrapper, key) {
    var return_value = wrapper.triggerHandler('beforeDelete', [key]);
    return (typeof return_value == 'undefined') || return_value;
}

function __jackfrost_singlechoice_after_del(wrapper, key) {
    var return_value = wrapper.triggerHandler('afterDelete', [key]);
    return (typeof return_value == 'undefined') || return_value;
}

/**
 *
 * Internal calls
 *
 */

function __jackfrost_singlechoice_setvalue(item, wrapper_text, wrapper_hidden) {
    if (!__jackfrost_singlechoice_before_set(wrapper_hidden, item)) return;
    wrapper_hidden.val(item.key);
    wrapper_text.addClass('ac-item-selected').prop("readonly", true).val(item.label);
    __jackfrost_singlechoice_after_set(wrapper_hidden, item);
}

function __jackfrost_singlechoice_delvalue(wrapper_text, wrapper_hidden) {
    var value = wrapper_hidden.val();
    if (!__jackfrost_singlechoice_before_del(wrapper_hidden, value)) return;
    wrapper_hidden.val('');
    wrapper_text.removeClass('ac-item-selected').prop("readonly", false).val('');
    __jackfrost_singlechoice_after_del(wrapper_hidden, value);
}

/**
 *
 * Constructor
 *
 */

function jackfrost_singlechoice($,
                                id,
                                autocomplete_source_url,
                                initialdata_source_url,
                                initialdata,
                                before_set,
                                after_set,
                                before_del,
                                after_del,
                                renderer
                               ){

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
                __jackfrost_singlechoice_setvalue(ui.item, wrapper_text, wrapper_hidden);
            }
        }).data( "autocomplete" )._renderItem = function(ul, item){
            return __jackfrost_autocomplete_render(wrapper_hidden, ul, item);
        };

        wrapper_text.keydown(function(e){
            if (e.which == 46 && hasvalue()) __jackfrost_singlechoice_delvalue(wrapper_text, wrapper_hidden);
        });

        if (initialdata != null)
        {
            var params = {value: initialdata};
            var callback = function(data){
                __jackfrost_singlechoice_setvalue(data, wrapper_text, wrapper_hidden);
            };
            $.get(initialdata_source_url, params, callback, 'json');
        }

        if (typeof before_del != 'undefined') wrapper_hidden.bind("beforeDelete", before_del);
        if (typeof after_del != 'undefined') wrapper_hidden.bind("afterDelete", after_del);
        if (typeof before_set != 'undefined') wrapper_hidden.bind("beforeSet", before_set);
        if (typeof after_set != 'undefined') wrapper_hidden.bind("afterSet", after_set);
        if (typeof renderer != 'undefined') wrapper_hidden.bind("render", renderer);
    });
}

/**
 *
 * JackFrost Singlechoice stuff end
 *
 */

/**
 *
 * JackFrost Multichoice stuff
 * * event handlers
 * * internal calls
 * * constructor
 *
 **/

/**
 *
 * Event handlers
 *
 */

function __jackfrost_multichoice_before_add(wrapper, listbox_wrapper, item) {
    var return_value = wrapper.triggerHandler('beforeAdd', [item.key, item]);
    return (typeof return_value == 'undefined') || return_value;
}

function __jackfrost_multichoice_after_add(wrapper, listbox_wrapper, item) {
    var return_value = wrapper.triggerHandler('afterAdd', [item.key, item]);
    return (typeof return_value == 'undefined') || return_value;
}

function __jackfrost_multichoice_before_rem(wrapper, listbox_wrapper, key, inlist_pos) {
    var return_value = wrapper.triggerHandler('beforeRemove', [listbox_wrapper[0], key, inlist_pos]);
    return (typeof return_value == 'undefined') || return_value;
}

function __jackfrost_multichoice_after_rem(wrapper, listbox_wrapper, key, inlist_pos) {
    var return_value = wrapper.triggerHandler('afterRemove', [listbox_wrapper[0], key, inlist_pos]);
    return (typeof return_value == 'undefined') || return_value;
}

/**
 *
 * Internal calls
 *
 */

var __jackfrost_multichoice_values_lists = {};

function __jackfrost_multichoice_get_values_list(hidden_id) {
    if (!(hidden_id in __jackfrost_multichoice_values_lists)) {
        __jackfrost_multichoice_values_lists[hidden_id] = [];
    }
    return __jackfrost_multichoice_values_lists[hidden_id];
}

var __jackfrost_multichoice_addvalue = function(item, wrapper_list, wrapper_text, wrapper_hidden) {
    var values = __jackfrost_multichoice_get_values_list(wrapper_hidden.attr('id'));
    var value = item.key;
    if (values.indexOf(value) > -1) return;
    if (!__jackfrost_multichoice_before_add(wrapper_hidden, wrapper_list, item)) return;
    values.push(item.key);
    wrapper_hidden.val(JSON.stringify(values));
    wrapper_list.append($('<option></option>').attr('value', item.key).text(item.label));
    __jackfrost_multichoice_after_add(wrapper_hidden, wrapper_list, item);
};

var __jackfrost_multichoice_remvalue = function(pos_array, wrapper_list, wrapper_hidden) {
    var values = __jackfrost_multichoice_get_values_list(wrapper_hidden.attr('id'));
    var key = values[pos_array];
    if (!__jackfrost_multichoice_before_rem(wrapper_hidden, wrapper_list, key, pos_array)) return;
    values.splice(pos_array, 1);
    wrapper_hidden.val(JSON.stringify(values));
    wrapper_list.children("option:selected").remove();
    __jackfrost_multichoice_after_rem(wrapper_hidden, wrapper_list, key, pos_array);
};

/**
 *
 * Constructor
 *
 */

function jackfrost_multichoice($,
                               id,
                               autocomplete_source_url,
                               initialdata_source_url,
                               initialdata,
                               before_add,
                               after_add,
                               before_rem,
                               after_rem,
                               renderer
                              ){

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
                __jackfrost_multichoice_addvalue(ui.item, wrapper_list, wrapper_text, wrapper_hidden);
            }
        }).data( "autocomplete" )._renderItem = function(ul, item){
            return __jackfrost_autocomplete_render(wrapper_hidden, ul, item);
        };

        wrapper_list.keydown(function(e){
            if (e.which == 46) {
                var items = wrapper_list.children("option");
                var positions = [];
                items.each(function(i, e) {
                    if ($(e).is(":selected")) positions.unshift(i);
                });
                if (positions.length > 0) {
                    for(var posind=0; posind < positions.length; posind++) {
                        __jackfrost_multichoice_remvalue(positions[posind], wrapper_list, wrapper_hidden);
                    }
                }
            }
        }).width(
            wrapper_text.width()
        ).css(
            'margin',
            wrapper_text.css('margin')
        ).css(
            'left',
            wrapper_text.css('left')
        );

        __jackfrost_multichoice_get_values_list(wrapper_hidden.attr('id'));
        wrapper_hidden.val("[]");
        if (initialdata != null)
        {
            var params = {value: initialdata};
            var callback = function(data){
                $.each(data, function(i, item){
                    __jackfrost_multichoice_addvalue(item, wrapper_list, wrapper_text, wrapper_hidden);
                });
            };
            $.post(initialdata_source_url, params, callback, 'json');
        }

        if (typeof before_rem != 'undefined') wrapper_hidden.bind("beforeRemove", before_rem);
        if (typeof after_rem != 'undefined') wrapper_hidden.bind("afterRemove", after_rem);
        if (typeof before_add != 'undefined') wrapper_hidden.bind("beforeAdd", before_add);
        if (typeof after_add != 'undefined') wrapper_hidden.bind("afterAdd", after_add);
        if (typeof renderer != 'undefined') wrapper_hidden.bind("render", renderer);
    });
}

/**
 *
 * JackFrost Multichoice stuff end
 *
 */