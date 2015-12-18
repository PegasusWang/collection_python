/*
 
	Awkward Showcase - jQuery plugin 
	http://www.jquery.com
	http://www.awkwardgroup.com/sandbox/awkward-showcase-a-jquery-plugin
	http://demo.awkwardgroup.com/showcase
	Version: 1.1.3

	Copyright (C) 2011 Awkward Group (http://www.awkwardgroup.com)
	Licensed under Attribution-ShareAlike 3.0 Unported
	http://creativecommons.org/licenses/by-sa/3.0/

	Markup example for jQuery("#showcase").awShowcase();
 
	<div id="showcase" class="showcase">
		<!-- Each child div in #showcase represents a slide -->
		<div class="showcase-slide">
			<!-- Put the slide content in a div with the class .showcase-content -->
			<div class="showcase-content">
				<!-- If the slide contains multiple elements you should wrap them in a div with the class .showcase-content-wrapper. 
				We usually wrap even if there is only one element, because it looks better. :-) -->
				<div class="showcase-content-wrapper">
					<img src="images/01.jpg" alt="01" />
				</div>
			</div>
			<!-- Put the caption content in a div with the class .showcase-caption -->
			<div class="showcase-caption">
				The Caption
			</div>
			<!-- Put the tooltips in a div with the class .showcase-tooltips. -->
			<div class="showcase-tooltips">
				<!-- Each anchor in .showcase-tooltips represents a tooltip. The coords attribute represents the position of the tooltip. -->
				<a href="http://www.awkward.se" coords="634,130">
					<!-- The content of the anchor-tag is displayed in the tooltip. -->
					This is a tooltip that displays the anchor html in a nice way.
				</a>
				<a href="http://www.awkward.se" coords="356, 172">
					<!-- You can add multiple elements to the anchor-tag which are display in the tooltip. -->
					<img src="images/glasses.png" />
					<span style="display: block; font-weight: bold; padding: 3px 0 3px 0; text-align: center;">
						White Glasses: 500$
					</span>
				</a>
			</div>
		</div>
		<div class="showcase-slide">
			<div class="showcase-content">
				<div class="showcase-content-wrapper">
					Content...
				</div>
			</div>
		</div>
	</div>

*/

(function(jQuery) {

	jQuery.fn.awShowcase = function(options) {
	
		// Default configuration properties
		var defaults =
		{
			content_width:			700,
			content_height:			470,
			fit_to_parent:			false,
			auto:					false,
			interval:				3000,
			continuous:				false,
			loading:				true,
			tooltip_width:			200,
			tooltip_icon_width:		32,
			tooltip_icon_height:	32,
			tooltip_offsetx:		18,
			tooltip_offsety:		0,
			arrows:					true,
			buttons:				true,
			btn_numbers:			false,
			keybord_keys:			false,
			mousetrace:				false, /* Trace x and y coordinates for the mouse */
			pauseonover:			true,
			stoponclick:			true,
			transition:				'hslide', /* hslide / vslide / fade */
			transition_delay:		300,
			transition_speed:		500,
			show_caption:			'onload', /* onload / onhover / show */
			thumbnails:				false,
			thumbnails_position:	'outside-last', /* outside-last / outside-first / inside-last / inside-first */
			thumbnails_direction:	'vertical', /* vertical / horizontal */
			thumbnails_slidex:		0, /* 0 = auto / 1 = slide one thumbnail / 2 = slide two thumbnails / etc. */
			dynamic_height:			false, /* For dynamic height to work in webkit you need to set the width and height of images in the source. Usually works to only set the dimension of the first slide in the showcase. */
			speed_change:			false, /* This prevents user from swithing more then one slide at once */
			viewline:				false, /* If set to true content_width, thumbnails, transition and dynamic_height will be disabled. As for dynamic height you need to set the width and height of images in the source. */
			fullscreen_width_x:		15,
			custom_function:		null
		};

		// *****************
		// SET UP THE PLUGIN
		// *****************
		
		// Declare and set up some important variables
		options = jQuery.extend(defaults, options);
		var current_id = 0;
		var previous_id = 0;
		var break_loop = false;
		var pause_loop = false;
		var myInterval = null;
		var showcase = jQuery(this);
		var showcase_width = options.content_width;
		var animating = false;
		// Viewline specific variables
		var content_viewline_width = 10000;
		var animation_distance = 0;
		var old_animation_distance = 0;
		var remaining_width = 0;
		
		// Set up the content wrapper
		var content_container = jQuery(document.createElement('div'))
			.css('overflow', 'hidden')
			.css('position', 'relative')
			.addClass('showcase-content-container')
			.prependTo(showcase);
			
		// Set up the showcase for hundred percent width
		if (options.fit_to_parent)
		{
			showcase_width = jQuery(showcase).width() + options.fullscreen_width_x;
		}
		
		// Set up the showcase for Viewline Mayhem
		if (options.viewline)
		{
			options.thumbnails = false;
			options.dynamic_height = false;
			content_container.css('width', content_viewline_width);
			showcase.css('overflow', 'hidden');
			$('.showcase-arrow-previous').hide();
		}
		
		// Set up content and create the content and thumbnail array
		var contentArray = [];
		var thumbnailArray = [];
		var content_count = 0;
		showcase.children('.showcase-slide').each(function()
		{
			// Get content
			var object = jQuery(this);
			content_count++;
	
			// If thumbnails are activated
			if (options.thumbnails)
			{
				// Get thumbnail and put in array
				var thumb = object.find('.showcase-thumbnail');
				thumbnailArray.push(thumb);
				thumb.remove();
			}
			
			// Set content width and height
			var object_width = object.find('.showcase-content').children().width();
			var object_height = object.find('.showcase-content').children().height();
			
			// Add content html in array and remove it from DOM
			contentArray.push(object.html());
			object.remove();
			
			// Get correct content
			var new_object = getContent(content_count-1);
			if (options.viewline || content_count === 1) { content_container.append(new_object); } 
			
			// Viewline setup
			if (options.viewline)
			{
				new_object.css('position', 'relative');
				new_object.css('float', 'left');
				new_object.css('width', object_width);
			}
			
			// Set content and content container load height
			if (options.dynamic_height)
			{
				new_object.css('height', object_height);
				if (content_count === 1) { content_container.css('height', object_height); }
			}
			else
			{
				new_object.css('height', options.content_height);
				if (content_count === 1) { content_container.css('height', options.content_height); }
			}
			
			if (options.viewline || content_count === 1)
			{
				displayAnchors(new_object);
				displayCaption(new_object);
				
				if (options.show_caption === 'show')
				{
					jQuery(new_object).find('.showcase-caption').show();
				}
			}
		});
		
		// Declare and set up the thumbnail wrapper
		var thumb_wrapper;
		var thumbnailStretch = 0;
		var thumbnailsPerPage = 0;
		if (options.thumbnails)
		{
			// Create wrapper
			thumb_container = jQuery('<div />');
			thumb_restriction = jQuery('<div />');
			thumb_wrapper = jQuery('<div />');
			
			// Add content to thumbnail wrapper
			for (i = thumbnailArray.length-1; i >= 0; --i)
			{
				var thumbnail = jQuery(thumbnailArray[i]).css({'overflow' : 'hidden'});
				thumbnail.attr('id', 'showcase-thumbnail-' + i);
				thumbnail.addClass((i === 0) ? 'active' : '');
				thumbnail.click(function(a, b)
				{
					// This function is used to extract the correct i value on click
					return function()
					{
						// Disable auto change on click
						if (myInterval) { pause_loop = true; clearInterval(myInterval); }
						changeContent(a, b);
					};
				}(i, ''));	
				thumb_wrapper.prepend(thumbnail);
			}
			
			// Style and position thumbnail container and content wrapper
			// + insert thumbnail container
			if (options.thumbnails_position === 'outside-first' || options.thumbnails_position === 'outside-last')
			{
				if (options.thumbnails_direction !== 'horizontal')
				{
					/* outside & vertical */
					content_container.css('float', 'left');
					content_container.css('width', options.content_width);
					thumb_container.css('float', 'left');
					thumb_container.css('height', options.content_height);
				}
				else
				{
					/* outside & horizontal */
					jQuery(thumb_wrapper).find('.showcase-thumbnail').css('float', 'left');
					//jQuery(thumb_wrapper).append(jQuery('<div />').addClass('clear'));
				}
				
				if (options.thumbnails_position === 'outside-last')
				{
					/* outside-last */
					showcase.append(thumb_container);
					if (options.thumbnails_direction !== 'horizontal') { showcase.append(jQuery('<div />').addClass('clear')); }
				}
				else
				{
					/* outside-first */
					showcase.prepend(thumb_container);
					if (options.thumbnails_direction !== 'horizontal') { showcase.append(jQuery('<div />').addClass('clear')); }
				}
			}
			else
			{
				thumb_container.css({'position' : 'absolute', 'z-index' : 20});
				if (options.thumbnails_direction === 'horizontal') 
				{
					/* inside & horizontal */
					thumb_container.css({'left' : 0, 'right' : 0});
					jQuery(thumb_wrapper).find('.showcase-thumbnail').css('float', 'left');
					jQuery(thumb_wrapper).append(jQuery('<div />').addClass('clear'));
					
					/* inside first */
					if (options.thumbnails_position === 'inside-first') { thumb_container.css('top', 0); }
					/* inside last */
					else { thumb_container.css('bottom', 0); }
				}
				else 
				{
					/* inside & vertical */
					thumb_container.css({'top' : 0, 'bottom' : 0});
					/* inside first */
					if (options.thumbnails_position === 'inside-first') { thumb_container.css('left', 0); }
					/* inside last */
					else { thumb_container.css('right', 0); }
				}
				content_container.prepend(thumb_container);
			}
			
			// Add class and style to thumbnail container
			thumb_container.addClass('showcase-thumbnail-container');
			thumb_container.css('overflow', 'hidden');
			
			// Add class and style to thumbnail restriction
			thumb_restriction.addClass('showcase-thumbnail-restriction');
			thumb_restriction.css({'overflow' : 'hidden', 'position' : 'relative'});
			if (options.thumbnails_direction === 'horizontal') { thumb_restriction.css({'float' : 'left'}); }
			
			// Add class and style to thumbnail wrapper 
			thumb_wrapper.addClass('showcase-thumbnail-wrapper');
			if (options.thumbnails_direction === 'horizontal') { thumb_wrapper.addClass('showcase-thumbnail-wrapper-horizontal'); }
			else { thumb_wrapper.addClass('showcase-thumbnail-wrapper-vertical'); }
			thumb_wrapper.css('position', 'relative');
			
			// Append wrapper and restriction
			thumb_restriction.append(thumb_wrapper);
			thumb_container.append(thumb_restriction);
			
			// Add backward button
			var buttonBackward = jQuery('<div class="showcase-thumbnail-button-backward" />');
			if (options.thumbnails_direction !== 'horizontal')
			{
				buttonBackward.html('<span class="showcase-thumbnail-vertical"><span>Up</span></span>');
			}
			else
			{
				buttonBackward.css({'float' : 'left'});
				buttonBackward.html('<span class="showcase-thumbnail-horizontal"><span>Left</span></span>');
			}
			buttonBackward.click(function() { slideThumbnailWrapper('backward', false, true); });
			thumb_container.prepend(buttonBackward);
			
			// Add forward button
			var buttonForward = jQuery('<div class="showcase-thumbnail-button-forward" />');
			if (options.thumbnails_direction !== 'horizontal')
			{
				buttonForward.html('<span class="showcase-thumbnail-vertical"><span>Down</span></span>');
			}
			else
			{
				buttonForward.css({'float' : 'left','padding-right' : '0'});
				buttonForward.html('<span class="showcase-thumbnail-horizontal"><span>Right</span></span>');
			}
			buttonForward.click(function() { slideThumbnailWrapper('forward', false, true); });
			thumb_container.append(buttonForward);
			
			// Set the number of thumbnails per page.
			var thumbnailVisibleStretch = 0;
			if (options.thumbnails_direction !== 'horizontal')
			{
				thumbnailVisibleStretch = getElementHeight(thumb_wrapper, false);
				thumbnailVisibleStretch += (getElementHeight(buttonBackward)) + (getElementHeight(buttonForward));
				while (thumbnailVisibleStretch < options.content_height)
				{
					thumbnailVisibleStretch += getElementHeight(jQuery(thumbnailArray[0]));
					thumbnailsPerPage++;
				}
			}
			else
			{
				thumbnailVisibleStretch = getElementWidth(thumb_wrapper, false);
				thumbnailVisibleStretch += (getElementWidth(buttonBackward)) + (getElementWidth(buttonForward));
				
				while (thumbnailVisibleStretch < showcase_width)
				{
					thumbnailVisibleStretch += getElementWidth(jQuery(thumbnailArray[0]));
					thumbnailsPerPage++;
				}
			}
			
			// Hide buttons if they're not necessary
			if (thumbnailsPerPage+1 > thumbnailArray.length)
			{
				if (options.thumbnails_direction !== 'horizontal')
				{
					thumb_restriction.css('margin-top', getElementHeight(buttonBackward));
				}
				else
				{
					//thumb_restriction.css('margin-left', getElementWidth(buttonBackward));
				}
				buttonBackward.hide();
				buttonForward.hide();
			}
			
			// Set thumbnail restriction height or width
			if (options.thumbnails_direction !== 'horizontal')
			{
				var buttonsHeight = (getElementHeight(buttonBackward)) + (getElementHeight(buttonForward));
				thumb_restriction.css('height', options.content_height - buttonsHeight);
			}
			else
			{
				var buttonsWidth = (getElementWidth(buttonBackward)) + (getElementWidth(buttonForward));
                if(buttonBackward.css('display')=="none"){
                    buttonsWidth = 0;
                }
				thumb_restriction.css('width',  showcase_width-buttonsWidth);
			}
			
			// Set thumbnail wrapper width
			if (options.thumbnails_direction === 'horizontal')
			{
				jQuery('.showcase-thumbnail').each(function() { thumbnailStretch += getElementWidth(jQuery(this)); });
				thumb_wrapper.css('width', thumbnailStretch);
			}
			else { jQuery('.showcase-thumbnail').each(function() { thumbnailStretch += getElementHeight(jQuery(this)); }); }
		}
		
		// Set showcase width and height
		if (options.thumbnails && options.thumbnails_position.indexOf("outside") !== -1 && options.thumbnails_direction !== 'horizontal' && !options.viewline)
		{
			showcase.css('width', showcase_width + getElementWidth(thumb_wrapper, true, false));
		}
		else if  (!options.fit_to_parent) { showcase.css('width', showcase_width); }
		
		// Turn on/off auto slide
		if (content_count > 1 && options.auto) { myInterval = window.setInterval(autoChange, options.interval); }
		
		// Pause auto on mouse over
		if (options.auto && options.pauseonover)
		{
			showcase.mouseenter(function() { break_loop = true; clearInterval(myInterval); });
			showcase.mouseleave(function()
			{
				if (!pause_loop)
				{
					break_loop = false; myInterval = window.setInterval(autoChange, options.interval);
				}
			});
		}
		
		// Adding navigation arrows
		if (options.arrows && content_count > 1)
		{
			// Left arrow
			jQuery(document.createElement('div'))
				.addClass('showcase-arrow-previous')
				.prependTo(showcase)
				.click(function() {
					// Disable auto change on click
					if (myInterval)
					{
						if (options.stoponclick) { pause_loop = true; }
						clearInterval(myInterval);
					}
					changeContent((current_id === 0) ? content_count-1 : parseInt(current_id)-1, 'previous');
				});
			// Right arrow
			jQuery(document.createElement('div'))
				.addClass('showcase-arrow-next')
				.prependTo(showcase)
				.click(function() {
					// Disable auto change on click
					if (myInterval)
					{
						if (options.stoponclick) { pause_loop = true; }
						clearInterval(myInterval);
					}
					changeContent(current_id+1, 'next');
				});
				
			if (options.viewline) { $('.showcase-arrow-previous').hide(); }
		}
		
		// Adding navigation buttons
		if (options.buttons && content_count > 1)
		{
			// Create button wrapper
			jQuery(document.createElement('div'))
				.css('clear', 'both')
				.addClass('showcase-button-wrapper')
				.appendTo(showcase);
			i = 0;
			// Add button for each content
			while (i < content_count)
			{
				jQuery(document.createElement('span'))
					.attr('id', 'showcase-navigation-button-' + i)
					.addClass((i === 0) ? 'active' : '')
					// Add numbers or unicode
					.html((options.btn_numbers) ? parseInt(i)+1 : '&#9679;')
					.click(function(a, b)
					{
						// This function is used to extract the correct i value on click
						return function()
						{
							// Disable auto change on click
							if (myInterval)
							{
								if (options.stoponclick) { pause_loop = true; }
								clearInterval(myInterval);
							}
							changeContent(a, b);
						};
					}(i, ''))
					.appendTo(jQuery(showcase).find('.showcase-button-wrapper'));
				i++;
			}
		}
		
		// Activating the keybord arrow keys
		if (options.keybord_keys)
		{
			jQuery(document).keydown(function(e)
			{
				// Disable auto change on click
				if (options.stoponclick) { pause_loop = true; }
				if (myInterval) clearInterval(myInterval);
				
				// Left arrow
				if (e.keyCode === 37) {
					changeContent((current_id === 0) ? content_count-1 : parseInt(current_id)-1, 'previous');
				}
				
				// Right arrow
				if (e.keyCode === 39) {
					changeContent((current_id === content_count-1) ? 0 : parseInt(current_id)+1, 'next');
				}
			});
		}
		
		
		// *************
		// THE FUNCTIONS
		// *************
		
		// Returns the specified content (by array id)
		function getContent(id) {
		
			var new_content = jQuery(document.createElement('div'))
				.attr('id', 'showcase-content-' + id)
				.css('overflow', 'hidden')
				.css('position', 'absolute')
				.addClass('showcase-content')
				.html(contentArray[id]);
			
			// Set content width
			if (!options.viewline) { new_content.css('width', options.content_width); }
			
			// Position the content wrapper if showcase width is set to hundred percent
			if (options.fit_to_parent && !options.viewline) { new_content.css('left', (showcase_width/2)-options.content_width/2); }
			
			return new_content;
		}
		
		// Function that runs when content is set to change automatically
		function autoChange() {
		
			// Set next content id
			var nextID = parseInt(current_id)+1;
			// If the next id is outside the array and continuous is set to true set the id to 0
			if (nextID === content_count && options.continuous) { nextID = 0; }
			// If continuous is set to false break the auto change
			else if (nextID === content_count && !options.continuous) { break_loop = true; clearInterval(myInterval); }
			// Don't change the content if the auto change is broken
			if (!break_loop) { changeContent(nextID, 'next'); }
		}
		
		// Changes the content (no explanation/comments needed :)
		function changeContent(id, direction) {
			
			// If the next content isn't the current content
			if (current_id !== id && !animating) {
				
				var obj;
				var obj2;
				var delay = 0;
				var i;
				
				// Set left/right position if showcase is set to full width
				var lrpos = (options.fit_to_parent) ? (showcase_width/2)-(options.content_width/2) : 0;
				
				// If we want to display the next content
				if ((id > current_id && direction !== 'previous') || direction === 'next') {
				
					if (options.viewline) {
						
						if (current_id < content_count-1) {
						
							// Prevent uggly transitions
							if (!options.speed_change) { animating = true; }
						
							// BugFix
							updateContentViewlineWidth();
								
							// Pause Autoplay
							if (options.pauseonover) { window.clearInterval(myInterval); }
							
							// First we check if the content will fill the screen after animation.
							remaining_width = 0;
							
							// Loop trough the content array to find out 
							// the total width for the content that remains.
							for (i=current_id+1, len=content_count; i<len; ++i)
							{
								obj = addedContentArray[i];
								remaining_width += obj.find('.showcase-content').children().width();
							}
							
							// If the remaining width is wider than the browser window.
							if (remaining_width > showcase_width)
							{
								old_animation_distance = animation_distance;
								animation_distance -= addedContentArray[current_id].find('.showcase-content').children().width();
							}
							else if ($('.showcase-arrow-next').is(':visible')) 
							{
								old_animation_distance = animation_distance;
								animation_distance = -(content_viewline_width - (remaining_width + (showcase_width - remaining_width)));
								$('.showcase-arrow-next').fadeOut(300);
							}
							
							content_container.animate({left: animation_distance + 'px'}, options.transition_speed, function() { animating = false; });
							
							// Change current content id (if content is finished)
							if ($('.showcase-arrow-next').is(':visible')) { current_id++; }
							
							$('.showcase-arrow-previous').fadeIn(300);
						}
					}
					else {
					
						// Prevent uggly transitions
						if (!options.speed_change) { animating = true; }
						
						// Get current and next content element
						obj = jQuery(showcase).find('#showcase-content-' + parseInt(current_id));
						obj2 = getContent(id);
						
						// Append next element and set height
						content_container.append(obj2);
						if (options.dynamic_height) { obj2.css('height', obj2.find('.showcase-content').children().height()); }
						else { obj2.css('height', options.content_height); }
						
						// Animate height first if next content is not as high
						if (obj.find('.showcase-content').children().height() > obj2.find('.showcase-content').children().height() && options.dynamic_height) {
						
							content_container.stop(true, true).animate({ height: obj2.find('.showcase-content').children().height() }, 200);
							delay = 100;
						}
						
						// Animate current element
						if (options.transition === 'hslide') {
						
							jQuery(obj).delay(delay).animate({ left: -(options.content_width) }, options.transition_speed+options.transition_delay, function() { obj.remove(); });
						}
						else if (options.transition === 'vslide') {
						
							jQuery(obj).delay(delay).animate({ top: -(options.content_height) }, options.transition_speed+options.transition_delay, function() { obj.remove(); });
						}
						else {
						
							jQuery(obj).delay(delay).fadeOut(options.transition_speed, function() { obj.remove(); });
						}
						
						// This will hide them, not display them :)
						displayAnchors(obj, true);
						displayCaption(obj, true);
						
						// Animate next element
						if (options.transition === 'hslide') {
						
							obj2.css('left', showcase_width);
							jQuery(obj2).delay(delay).animate({ left: lrpos }, options.transition_speed, function() {
									displayAnchors(obj2);
									displayCaption(obj2);
									afterAnimation(obj2);
								}
							);
						}
						else if (options.transition === 'vslide') {
						
							obj2.css('top', showcase.height());
							jQuery(obj2).delay(delay).animate({ top: '0px' }, options.transition_speed, function() {
									displayAnchors(obj2);
									displayCaption(obj2);
									afterAnimation(obj2);
								}
							);
						}
						else {
							
							obj2.css('left', lrpos);
							obj2.css('display', 'none');
							jQuery(obj2).delay(delay).fadeIn(options.transition_speed, function()
								{
									displayAnchors(obj2);
									displayCaption(obj2);
									afterAnimation(obj2);
								}
							);
						}
					}
				}
				// If we want to display the previous content
				else if (id < current_id || direction === 'previous') {
					
					if (options.viewline) {
					
						if (current_id !== 0) {
						
							// Prevent uggly transitions
							if (!options.speed_change) { animating = true; }
							
							// BugFix
							updateContentViewlineWidth();
							
							// Pause Autoplay
							if (options.pauseonover) { window.clearInterval(myInterval); }
							
							content_container.animate({left: old_animation_distance + 'px'}, options.transition_speed, function() { animating = false; });
							
							// Set animation distance
							animation_distance = old_animation_distance;
							
							// Change current content id
							current_id--;
							
							if (current_id === 0) { $('.showcase-arrow-previous').fadeOut(300); }
							
							// Set old distance
							old_id = current_id - 1;
							sub_width = jQuery(addedContentArray[old_id]).width();
							old_animation_distance = old_animation_distance + sub_width;
						}
						
						$('.showcase-arrow-next').fadeIn(300);
					}
					else {
					
						// Prevent uggly transitions
						if (!options.speed_change) { animating = true; }
						
						// Get current and next content element
						obj = jQuery(showcase).find('#showcase-content-' + parseInt(current_id));
						obj2 = getContent(id);
						
						// Append next element and set height
						content_container.append(obj2);
						if (options.dynamic_height) { obj2.css('height', obj2.find('.showcase-content').children().height()); }
						else { obj2.css('height', options.content_height); }
						
						// Animate height first if next content is not as high
						if (obj.find('.showcase-content').children().height() > obj2.find('.showcase-content').children().height() && options.dynamic_height) {
						
							content_container.stop(true, true).animate({ height: obj2.find('.showcase-content').children().height()}, 200);
							delay = 100;
						}
						
						// Animate current element
						if (options.transition === 'hslide') {
						
							jQuery(obj).delay(delay).animate({
								left: (showcase_width) + 'px'
								}, options.transition_speed+options.transition_delay, function() {
									displayAnchors(obj, true);
									displayCaption(obj, true);
									obj.remove();
							});
						}
						else if (options.transition === 'vslide') {
						
							jQuery(obj).delay(delay).animate({
								top: (options.content_height) + 'px'
								}, options.transition_speed+options.transition_delay, function(){
									displayAnchors(obj, true);
									displayCaption(obj, true);
									obj.remove();
							});
						}
						else {
						
							jQuery(obj).delay(delay).fadeOut(options.transition_speed, function() {
								displayAnchors(obj, true);
								displayCaption(obj, true);
								obj.remove();
							});
						}
						
						// Animate next element
						if (options.transition === 'hslide')
						{
							obj2.css('left', '-' + options.content_width + 'px');
							jQuery(obj2).delay(delay).animate({
								left: lrpos
								}, options.transition_speed, function() {
									displayAnchors(obj2);
									displayCaption(obj2);
									afterAnimation(obj2);
							});
						}
						else if (options.transition === 'vslide')
						{
							obj2.css('top', '-' +  showcase.height() + 'px');
							jQuery(obj2).delay(delay).animate({
								top: '0px'
								}, options.transition_speed, function() {
									displayAnchors(obj2);
									displayCaption(obj2);
									afterAnimation(obj2);
							});
						}
						else 
						{
							obj2.css('left', lrpos);
							obj2.css('display', 'none');	
							jQuery(obj2).delay(delay).fadeIn(options.transition_speed, function() {
								displayAnchors(obj2);
								displayCaption(obj2);
								afterAnimation(obj2);
							});
						}
						content_container.append(obj2);
					}
				}
				
				if(!options.viewline)
				{
					// Change previous and current content id
					previous_id = current_id;
					current_id = id;
							
					// Slide thumbnail wrapper
					if (options.thumbnails)
					{
						if ((current_id > previous_id && direction !== 'previous') || direction === 'next')
						{
							slideThumbnailWrapper('forward', true);
						}
						else if (current_id < previous_id || direction === 'previous')
						{
							slideThumbnailWrapper('backward', true);
						}
					}
					
					// Change click handlers for arrows
					if (options.arrows)
					{
						jQuery(showcase).find('.showcase-arrow-previous')
							.unbind('click')
							.click(function() {
								if (myInterval)
								{
									if (options.stoponclick) { pause_loop = true; }
									clearInterval(myInterval);
								}
								changeContent((current_id === 0) ? content_count-1 : parseInt(current_id)-1, 'previous');
							});
							jQuery(showcase).find('.showcase-arrow-next')
							.unbind('click')
							.click(function() {
								if (myInterval)
								{
									if (options.stoponclick) { pause_loop = true; }
									clearInterval(myInterval);
								}
								changeContent((current_id === content_count-1) ? 0 : parseInt(current_id)+1, 'next');
							});
					}
					
					// Change active class for thumbnails
					if (options.thumbnails)
					{
						i = 0;
						showcase.find('.showcase-thumbnail').each(function()
						{
							var object = jQuery(this);
							object.removeClass('active');
							if (i === current_id) { object.addClass('active'); }
							i++;
						});
					}
					
					// If caption is set to 'show'
					if (options.show_caption === 'show') { jQuery(obj2).find('.showcase-caption').show(); }
				}
				
				// Change active class for buttons
				if (options.buttons)
				{
					i = 0;
					showcase.find('.showcase-button-wrapper span').each(function()
					{
						var object = jQuery(this);
						object.removeClass('active');
						if (i === current_id) { object.addClass('active'); }
						i++;
					});
				}
					
				// A function that runs on content change, if it exists.
				if (typeof options.custom_function == 'function')
				{ 	
					options.custom_function();
				}
			}
		}
		
		function afterAnimation(obj)
		{
			if (options.dynamic_height) { content_container.stop(true, true).animate({ height: obj.find('.showcase-content').children().height() }, 200); }
			animating = false;
		}
		
		// Slide thumbnail wrapper
		var thumbnailSlidePosition = 0;
		function slideThumbnailWrapper(direction, check, backwardforward)
		{
			var doTheSlide = true;
			var thumbnailHeightOrWidth = getElementHeight(jQuery(thumb_wrapper).find('.showcase-thumbnail'));
			if (options.thumbnails_direction === 'horizontal')
			{
				thumbnailHeightOrWidth = getElementWidth(jQuery(thumb_wrapper).find('.showcase-thumbnail'));
			}
			var multiplySlidePosition = 1;
			
			// Set slide x
			if (options.thumbnails_slidex === 0) { options.thumbnails_slidex = thumbnailsPerPage; }
			
			// Check if we need to do the slide
			if (check)
			{
				var thumbnailSlidePositionCopy = thumbnailSlidePosition;
				var thumbnailsScrolled = 0;
				while (thumbnailSlidePositionCopy < 0)
				{
					if (options.thumbnails_direction === 'horizontal')
					{
						thumbnailSlidePositionCopy += getElementWidth(jQuery(thumbnailArray[0]));
					}
					else
					{
						thumbnailSlidePositionCopy += getElementHeight(jQuery(thumbnailArray[0]));
					}
					thumbnailsScrolled++;
				}
				
				var firstVisible = thumbnailsScrolled;
				var lastVisible = thumbnailsPerPage + thumbnailsScrolled -1;
				
				// Check if the next active thumbnail is outside the visible area
				if (current_id >= firstVisible && current_id <= lastVisible) { doTheSlide = false; }
				
				// If the next active thumbnail is far away..
				var distance;
				if ((current_id - lastVisible) > options.thumbnails_slidex)
				{
					distance = current_id - lastVisible;
					
					while (distance > options.thumbnails_slidex)
					{
						distance -= options.thumbnails_slidex;
						multiplySlidePosition++;
					}
				}
				else if ((firstVisible - current_id) > options.thumbnails_slidex)
				{
					distance =  firstVisible - current_id;
					
					while (distance > options.thumbnails_slidex)
					{
						distance -= options.thumbnails_slidex;
						multiplySlidePosition++;
					}
				}
				else { multiplySlidePosition = 1; }
			}
			
			if (direction === 'forward' && doTheSlide)
			{
				if (options.thumbnails_direction === 'vertical' && options.content_height < (thumbnailStretch + thumbnailSlidePosition))
				{
					thumbnailSlidePosition -= thumbnailHeightOrWidth * (options.thumbnails_slidex * multiplySlidePosition);
				}
				else if (options.thumbnails_direction === 'horizontal' && options.content_width < (thumbnailStretch + thumbnailSlidePosition))
				{
					thumbnailSlidePosition -= thumbnailHeightOrWidth * (options.thumbnails_slidex * multiplySlidePosition);
				}
				else if (current_id === 0)
				{
					if (!backwardforward) { thumbnailSlidePosition = 0; }
				}
				if (options.thumbnails_direction === 'horizontal') { thumb_wrapper.animate({ left: thumbnailSlidePosition }, 300); }
				else { thumb_wrapper.animate({ top: thumbnailSlidePosition }, 300); }
			}
			else if (doTheSlide)
			{
				if (thumbnailSlidePosition < 0)
				{
					thumbnailSlidePosition += thumbnailHeightOrWidth * (options.thumbnails_slidex * multiplySlidePosition);
				}
				else if (current_id === content_count-1)
				{
					if (!backwardforward)
					{
						thumbnailSlidePosition -= thumbnailHeightOrWidth * (options.thumbnails_slidex * multiplySlidePosition);
					}
				}
				else { thumbnailSlidePosition = 0; }
				if (options.thumbnails_direction === 'horizontal') { thumb_wrapper.animate({ left: thumbnailSlidePosition }, 300); }
				else { thumb_wrapper.animate({ top: thumbnailSlidePosition }, 300); }
			}
		}
		
		// Displays the caption
		function displayCaption(container, fadeOut)
		{
			var caption = container.find('.showcase-caption');
			if (!fadeOut)
			{
				if (options.show_caption === 'onload') { caption.fadeIn(300); }
				else if (options.show_caption === 'onhover')
				{
					jQuery(container).mouseenter(function()
					{
						caption.fadeIn(300);
					});
					
					jQuery(container).mouseleave(function()
					{
						caption.stop(true, true).fadeOut(100);
					});
				}
			}
			else { caption.stop(true, true).fadeOut(300); }
		}
		
		// Displays the anchors in the current slide
		function displayAnchors(container, fadeOut)
		{
			// Get each anchor tooltip
			container.find('.showcase-tooltips a').each(function()
			{
				if (!fadeOut)
				{
					// Get coordinates
					var coords = jQuery(this).attr('coords');
					coords = coords.split(',');
					
					// Style and position anchor
					jQuery(this).addClass('showcase-plus-anchor');
					jQuery(this).css('position', 'absolute');
					jQuery(this).css('display', 'none');
					jQuery(this).css('width', options.tooltip_icon_width);
					jQuery(this).css('height', options.tooltip_icon_height);
					jQuery(this).css('left', parseInt(coords[0]) - (parseInt(options.tooltip_icon_width)/2));
					jQuery(this).css('top', parseInt(coords[1]) - (parseInt(options.tooltip_icon_height)/2));
					var content = jQuery(this).html();
					jQuery(this).mouseenter(function()
					{
						animateTooltip(container, coords[0], coords[1], content);
					});
					jQuery(this).mouseleave(function()
					{
						animateTooltip(container, coords[0], coords[1], content);
					});
					jQuery(this).html('');
					jQuery(this).fadeIn(300);
				}
				else
				{
					jQuery(this).stop(true, true).fadeOut(300);
				}
			});
		}
		
		// Controls the animation for the tooltips
		var tooltip = null;
		function animateTooltip(container, x, y, content)
		{
			// if tooltip is null (doesn't exsist)
			if (tooltip === null)
			{
				// Create the tooltip
				tooltip = jQuery(document.createElement('div'))
					.addClass('showcase-tooltip')
					.css('display', 'none')
					.css('position', 'absolute')
					.css('max-width', options.tooltip_width)
					.html(content);
				container.append(tooltip);
				
				// Position the tooltip (this is where we try not to display the tooltip outside the content wrapper)
				var tooltip_paddingx = parseInt(tooltip.css('padding-right'))*2 + parseInt(tooltip.css('border-right-width'))*2;
				var tooltip_paddingy = parseInt(tooltip.css('padding-bottom'))*2 + parseInt(tooltip.css('border-bottom-width'))*2;
				lastx = parseInt(x) + tooltip.width() + tooltip_paddingx;
				lasty = parseInt(y) + tooltip.height() + tooltip_paddingy;
				
				if (lastx < options.content_width)
				{
					tooltip.css('left', parseInt(x) + parseInt(options.tooltip_offsetx));
				}
				else
				{
					tooltip.css('left', (parseInt(x) - parseInt(options.tooltip_offsetx)) - (parseInt(tooltip.width()) + parseInt(options.tooltip_offsetx)));
				}
				
				if (lasty < options.content_height)
				{
					tooltip.css('top', parseInt(y) + parseInt(options.tooltip_offsety));
				}
				else
				{
					tooltip.css('top', (parseInt(y) - parseInt(options.tooltip_offsety)) - (parseInt(tooltip.height()) + parseInt(tooltip_paddingy)));
				}
				
				// Fade in the tooltip
				tooltip.fadeIn(400);
			}
			else
			{
				// Fade out the tooltip
				tooltip.fadeOut(400);
				// Remove it from the DOM
				tooltip.remove();
				// And set the variable to null
				tooltip = null;
			}
		}
		
		/* Returns the correct height for the element, including padding and borders. */
		function getElementHeight(el, incHeight, incMargin, incPadding, incBorders)
		{
			incHeight = typeof(incHeight) !== 'undefined' ? incHeight : true;
			incMargin = typeof(incMargin) !== 'undefined' ? incMargin : true;
			incPadding = typeof(incPadding) !== 'undefined' ? incPadding : true;
			incBorders = typeof(incBorders) !== 'undefined' ? incBorders : true;
			var elHeight = (incHeight) ? jQuery((el)).height() : 0;
			var elMargin = 0;
			if ( incMargin ) {
			
				if ( jQuery( el ).css('margin-left') !== 'auto' ) { elMargin = parseFloat( jQuery( el ).css('margin-left') ); }
				if ( jQuery( el ).css('margin-right') !== 'auto' ) { elMargin += parseFloat( jQuery( el ).css('margin-right') ); }
			}
			elPadding = 0;
			if ( incPadding ) {
			
				if ( jQuery( el ).css('padding-left') !== 'auto' ) { elPadding = parseFloat( jQuery( el ).css('padding-left') ); }
				if ( jQuery( el ).css('padding-right') !== 'auto' ) { elPadding += parseFloat( jQuery( el ).css('padding-right') ); }
			}
			elBorder = 0;
			if ( incBorders ) {
			
				if ( jQuery( el ).css('border-left-width') !== 'auto' ) { elBorder = parseFloat( jQuery( el ).css('border-left-width') ); }
				if ( jQuery( el ).css('border-right-width') !== 'auto' ) { elBorder += parseFloat( jQuery( el ).css('border-right-width') ); }
			}
			elHeight += elMargin + elPadding + elBorder;
			return elHeight;
		}
		
		/* Returns the correct width for the element, including width, margin, padding and borders. */
		function getElementWidth(el, incWidth, incMargin, incPadding, incBorders)
		{
			incWidth = typeof(incWidth) !== 'undefined' ? incWidth : true;
			incMargin = typeof(incMargin) !== 'undefined' ? incMargin : true;
			incPadding = typeof(incPadding) !== 'undefined' ? incPadding : true;
			incBorders = typeof(incBorders) !== 'undefined' ? incBorders : true;
			var elWidth = (incWidth) ? jQuery((el)).width() : 0;
			var elMargin = 0;
			if ( incMargin ) {
			
				if ( jQuery( el ).css('margin-left') !== 'auto' ) { elMargin = parseFloat( jQuery( el ).css('margin-left') ); }
				if ( jQuery( el ).css('margin-right') !== 'auto' ) { elMargin += parseFloat( jQuery( el ).css('margin-right') ); }
			}
			elPadding = 0;
			if ( incPadding ) {
			
				if ( jQuery( el ).css('padding-left') !== 'auto' ) { elPadding = parseFloat( jQuery( el ).css('padding-left') ); }
				if ( jQuery( el ).css('padding-right') !== 'auto' ) { elPadding += parseFloat( jQuery( el ).css('padding-right') ); }
			}
			elBorder = 0;
			if ( incBorders ) {
			
				if ( jQuery( el ).css('border-left-width') !== 'auto' ) { elBorder = parseFloat( jQuery( el ).css('border-left-width') ); }
				if ( jQuery( el ).css('border-right-width') !== 'auto' ) { elBorder += parseFloat( jQuery( el ).css('border-right-width') ); }
			}
			elWidth += elMargin + elPadding + (elBorder || 0);
			return elWidth;
		}
		
		// Traces the mouse position (used for positioning anchors)
		if (options.mousetrace)
		{
			// Create the div tha displays the coordinates
			var mousetrace = jQuery(document.createElement('div'))
				.css('position', 'absolute')
				.css('top', '0')
				.css('background-color', '#fff')
				.css('color', '#000')
				.css('padding', '3px 5px')
				.css('x-index', '30')
				.html('X: 0 Y: 0');
			showcase.append(mousetrace);
			var offset = showcase.offset();
			
			// Print the coordinates
			content_container.mousemove(function(e){ mousetrace.html('X: ' + (e.pageX - offset.left)  + ' Y: ' + (e.pageY - offset.top)); });
		}
		
		// Show all content on one page
		$('#awOnePageButton').click(function showInOnePage()
		{
			if ($('.view-page').is(':visible'))
			{
				var temp_container = jQuery(document.createElement('div'));
				temp_container.addClass('showcase-onepage');
				showcase.before(temp_container);
				
				// Disable auto change on click
				if (myInterval) { pause_loop = true; clearInterval(myInterval); }
				
				$(this).find('.view-page').hide();
				$(this).find('.view-slide').show();
				showcase.hide();
			
				$.each(contentArray, function(index, value)
				{
					obj = getContent(index);
					obj.css('position', 'relative');
					temp_container.append(obj);
					
					displayAnchors(obj);
					displayCaption(obj);
					
					if (options.dynamic_height) { obj.css('height', obj.find('.showcase-content').children().height()); }
					else { obj.css('height', options.content_height); }
				});
				
				var clear = jQuery(document.createElement('div'));
				clear.addClass('clear');
				temp_container.append(clear);
			}
			else
			{
				$('.showcase-onepage').remove();
				$(this).find('.view-page').show();
				$(this).find('.view-slide').hide();
				showcase.show();
			}
			
			return false;
		});
		
		// The correct width is returned when all content is fully loaded.
		var addedContentArray = [];
		function updateContentViewlineWidth()
		{
			content_viewline_width = 0;
			content_container.children('div').each(function()
			{
				content_viewline_width += $(this).find('.showcase-content').children().width();
				addedContentArray.push($(this));
			});
		}
		
		// Remove loading class
		showcase.removeClass('showcase-load');
	};

})(jQuery);
