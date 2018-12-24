// sidebar-hider
$(document).ready(function() {
  $('#sidebarCollapse').on('click', function() {
    $('#sidebar').toggleClass('active');

    var $el = $(this),
      textNode = this.lastChild;
    $el.find('span').toggleClass('fa-chevron-left fa-chevron-right');
  });
});
