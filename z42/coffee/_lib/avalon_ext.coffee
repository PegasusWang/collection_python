
$.ajax_submit = (url, view, callback, failed) ->
    errtip = 0
    ->
        if this.tagName == "FORM"
            form = $ this
        else
            form = $(this).parents('form')
        errtip = errtip or $.errtip(form)
        form.find('input').each(->
            @value = @value
        )
        submit = form.find('input[type=submit]')

        disable = 'ui-button-disable'
        submit.addClass(disable)
        ##console.log view.o.$model,"!!"
        $.postJSON1 url, view.o.$model, (r) ->
            submit.removeClass(disable)
            errtip.reset()
            if r.err
                errtip.set(r.err)
                failed?(r.err)
            else
                callback r
        return false
