
window.def_view = _def_view = (id, ctrl)->
    avalon.define(
        id,
        ctrl
    )

$ ->
    window.def_view = (id, ctrl)->
        v = _def_view(id,ctrl)
        avalon.scan()
        return v

window.def_edit_view = (name, callback) ->
    def_view(
        name
        (v) ->
            v.is_edit = 0
            v.edit = ->
                V[name].is_edit = 1
            v.cancel = ->
                V[name].is_edit = 0
            callback(v)
    )
