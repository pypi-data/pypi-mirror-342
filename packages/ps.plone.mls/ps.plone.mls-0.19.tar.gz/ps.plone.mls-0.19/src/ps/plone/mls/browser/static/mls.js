jQuery(function(jq) {

  if (jq('.mls .development__gallery .thumbnails').length > 0) {
    // Build JS Gallery for development detail view.

    // Load the theme ones more. This is necessary for mobile devices.
    Galleria.loadTheme('++resource++plone.mls.listing.javascript/classic/galleria.classic.min.js');
    jq('.mls .development__gallery .thumbnails').before('<div id="galleria" class="development__galleria"></div>');

    // Hide the thumbnails
    jq('.mls .development__gallery .thumbnails').hide();

    // Initialize Galleria.
    var galleria_obj = jq('#galleria').galleria({
      dataSource: '.thumbnails',
      width: 'auto',
      height: 400,
      preload: 3,
      transition: 'fade',
      transitionSpeed: 1000,
      autoplay: 5000
    });
  }

  jq('.listingsearchbanner input').each(function() {
    var label = jq("label[for='" + jq(this).attr('id') + "']");
    this.placeholder = jq.trim(label.text());
  });

  jq('.listingsearchbanner label').each(function() {
    jq(this).hide();
  });

  /*
  Begin section
  PLONE 5 - Search button changes
  The pat-autotoc and autotabs classes are specific to the Plone 5 implementation
  */
  // Change search button into to use search icon
  jq('.listingsearchbanner .container .pat-autotoc.autotabs .formControls input').each(function() {
    jq(this).attr({
      type: 'hidden',
      alt: jq(this).attr('value'),
    });
    jq(this).after('<input type="image" src="++resource++ps.plone.mls/icons/search-icon-white.png" alt=' + jq(this).attr('value') + ' id=' + jq(this).attr('id') + '-icon >');
  });

  // Rearrange Search Button
  // Section 1
  var elem = jq('.listingsearchbanner .container .pat-autotoc.autotabs #form-section_1 .formControls');
  if(elem.length > 0) {
    elem.appendTo('.listingsearchbanner .container .pat-autotoc.autotabs #formfield-form-section_1-widgets-q');
  }

  // Section 2
  elem = jq('.listingsearchbanner .container .pat-autotoc.autotabs #form-section_2 .formControls');
  if(elem.length > 0) {
    elem.appendTo('.listingsearchbanner .container .pat-autotoc.autotabs #formfield-form-section_2-widgets-q');
  }

  // Section 3
  elem = jq('.listingsearchbanner .container .pat-autotoc.autotabs #form-section_3 .formControls');
  if(elem.length > 0) {
    elem.appendTo('.listingsearchbanner .container .pat-autotoc.autotabs #formfield-form-section_3-widgets-q');
  }

  // Section 4
  elem = jq('.listingsearchbanner .container .pat-autotoc.autotabs #form-section_4 .formControls');
  if(elem.length > 0) {
    elem.appendTo('.listingsearchbanner .container .pat-autotoc.autotabs #formfield-form-section_4-widgets-q');
  }
  /*
  End section
  PLONE 5 - Search button changes
  */

  // Plone 4:
  jq('.listingsearchbanner .z3cformInlineValidation').removeClass('z3cformInlineValidation');
  jq('.portletAgentContact .z3cformInlineValidation').removeClass('z3cformInlineValidation');
  jq('.portletQuickSearch .z3cformInlineValidation').removeClass('z3cformInlineValidation');
  jq('.listing-search-tile .z3cformInlineValidation').removeClass('z3cformInlineValidation');
  // Plone 5:
  jq('.listingsearchbanner .pat-inlinevalidation').removeClass('pat-inlinevalidation');
  jq('.portletAgentContact .pat-inlinevalidation').removeClass('pat-inlinevalidation');
  jq('.portletQuickSearch .pat-inlinevalidation').removeClass('pat-inlinevalidation');
  jq('.listing-search-tile .pat-inlinevalidation').removeClass('pat-inlinevalidation');

  if (jq('.listing__results div.results').length > 0) {
    // Hide the form when search was performed and show the edit form options link.
    jq('div.results form').hide();
    jq('div.results .listing__form-toggle').show();
    jq('div.results .listing__form-toggle a').click(function(event) {
      event.preventDefault();
      jq('div.results form').slideToggle();
    });
  }

});
