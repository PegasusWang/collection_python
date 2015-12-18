window.V = avalon.vmodels

window.View = (id, o, view)->
    o['$id'] = id
    v = avalon.define(
        o
    )
    view?(v)
    avalon.scan()
    v
