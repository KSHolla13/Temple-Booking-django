
jQuery("#simple-carousel").owlCarousel({
    rewind: true, /* use rewind if you don't want loop */
    margin: 20,
     /*
    animateOut: 'fadeOut',
    animateIn: 'fadeIn',
    */
    responsiveClass: true,
    // autoHeight: true,
    autoplayTimeout: 7000,
    smartSpeed: 800,
    nav: true,
    responsive: {
        0: {
          items: 1
        },
        360: {
          items: 1
        },
        768: {
          items: 1
        },
        991: {
          items: 1
        },
        1200: {
          items: 1
        },
        1920: {
          items: 1
        }
      }
  });

  
jQuery("#festival-carousel").owlCarousel({
  rewind: true, /* use rewind if you don't want loop */
  margin: 20,
   /*
  animateOut: 'fadeOut',
  animateIn: 'fadeIn',
  */
  responsiveClass: true,
  // autoHeight: true,
  autoplayTimeout: 7000,
  smartSpeed: 800,
  nav: true,
  responsive: {
      0: {
        items: 1
      },
      360: {
        items: 1
      },
      768: {
        items: 1
      },
      991: {
        items: 1
      },
      1200: {
        items: 1
      },
      1920: {
        items: 1
      }
    }
});
    
  jQuery("#venue-carousel").owlCarousel({
    rewind: true, /* use rewind if you don't want loop */
    margin: 20,
     /*
    animateOut: 'fadeOut',
    animateIn: 'fadeIn',
    */
    responsiveClass: true,
    // autoHeight: true,
    autoplayTimeout: 7000,
    smartSpeed: 800,
    nav: true,
    responsive: {
        0: {
          items: 1
        },
        360: {
          items: 1
        },
        768: {
          items: 2
        },
        991: {
          items: 2
        },
        1200: {
          items: 3
        },
        1920: {
          items: 3
        }
      }
  });