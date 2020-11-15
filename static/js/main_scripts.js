$( document ).on( 'click', '.tab-content a', function(event) {
   if (event.target.hasAttribute('href')) {
       var link = event.target.href + 'ajax/';
       var link_array = link.split('/');
       if (link_array[4] == 'category') {
           $.ajax({
               url: link,
               success: function (data) {
                   $('.tab-content').html(data.result);
               },
           });

           event.preventDefault();
       }
   }
});
