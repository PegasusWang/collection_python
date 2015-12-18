$.slide = (option) ->
  if $._slide
    $.slide.close ->
      $.slide option
  body = $("body")
  width = option.width | 860
  $._slide = slide = $("<div id=\"slideDown\"></div><div id=\"slide\" style=\"width:" + width + "px;margin-right:-" + (width + 6) + "px\">" + option.html + "</div>")
  body.after slide
  option.before_slide()  if option.before_slide?
  setTimeout (->
    body.addClass "slideBlur"
    $("#slideDown").click ->
      body.removeClass "slideBlur"
      $.slide.close()
    $("#slide").css "margin-right": null
  ), 50
$.slide.close = (callback) ->
  $._slide.remove()
  delete $._slide
  (if typeof callback is "function" then callback() else undefined)