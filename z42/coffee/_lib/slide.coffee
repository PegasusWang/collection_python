html = $("html")

$.slide = (option) ->
  if $._slide
    $.slide.close ->
      $.slide option
    return
  bg = $("#MAIN")
  body = $("body")
  width = option.width
  $._slide = slide = $("<div id=\"slideDown\"><div id=\"slide\" style=\"width:" + width + "px;margin-right:-" + (width + 6) + "px\">" + option.html + "</div></div>")
  body.append slide

  option.before_slide?()

  bg.addClass "slideBlur"
        
  setTimeout (
      ->
        $("#slide").css "margin-right", 0
  )
  # hack for safari 底面模糊很奇怪
  main = $("#MAIN")
  top = -html.scrollTop()
  main.css(marginTop: top)
  html.css('overflow',"hidden")
  setTimeout (
    ->
        option.after_show?()
        $("#slideDown").click (e)->
          if e.target == this
              bg.removeClass "slideBlur"
              $.slide.close()
  )

  $.slide.close = (callback) ->
    option?.before_close()
    $._slide.remove()
    delete $._slide
    html.css {overflow:"visible"}
    main.css(marginTop:0)
    (if typeof callback is "function" then callback() else undefined)


$.slide.close = ->

