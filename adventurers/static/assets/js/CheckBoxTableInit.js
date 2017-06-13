
 //
// Updates "Select all" control in a data table
//
function updateDataTableSelectAllCtrl(table){
var $table             = table.table().node();
var $chkbox_all        = $('tbody input[type="checkbox"]', $table);
var $chkbox_checked    = $('tbody input[type="checkbox"]:checked', $table);
var chkbox_select_all  = $('thead input[name="select_all"]', $table).get(0);

// If none of the checkboxes are checked


}

$(document).ready(function (){
// Array holding selected row IDs
var rows_selected = [];
var table = $('#mainTable').DataTable({
       dom: 'Bfrtip',
     buttons: [
         {
             text: 'Select all',
             action: function () {
                 table.rows().select();
             }
         },
         {
             text: 'Select none',
             action: function () {
                 table.rows().deselect();
             }
         }
     ],
   'columnDefs': [{
      'targets': 0,
      'searchable': false,
      'orderable': false,
      'width': '1%',
       className: 'select-checkbox',
      'render': function (data, type, full, meta){
          return '<input type="checkbox">';
      }
    }],
   'order': [[4, 'desc']],
   'rowCallback': function(row, data, dataIndex){
      // Get row ID
      var rowId = data[0];

      // If row ID is in the list of selected row IDs
      if($.inArray(rowId, rows_selected) !== -1){
         $(row).find('input[type="checkbox"]').prop('checked', true);
         $(row).addClass('selected');
      }
   }
});

// Handle click on checkbox
$('#mainTable tbody').on('click', 'input[type="checkbox"]', function(e){
   var $row = $(this).closest('tr');

   // Get row data
   var data = table.row($row).data();

   // Get row ID
   var rowId = data[0];

   // Determine whether row ID is in the list of selected row IDs
   var index = $.inArray(rowId, rows_selected);

   // If checkbox is checked and row ID is not in list of selected row IDs
   if(this.checked && index === -1){
      rows_selected.push(rowId);

   // Otherwise, if checkbox is not checked and row ID is in list of selected row IDs
   } else if (!this.checked && index !== -1){
      rows_selected.splice(index, 1);
   }

   if(this.checked){
      $row.addClass('selected');
   } else {
      $row.removeClass('selected');
   }

   // Update state of "Select all" control
   updateDataTableSelectAllCtrl(table);

   // Prevent click event from propagating to parent
   e.stopPropagation();
});

// Handle click on table cells with checkboxes
$('#mainTable').on('click', 'tbody td, thead th:first-child', function(e){
   $(this).parent().find('input[type="checkbox"]').trigger('click');
});

// Handle click on "Select all" control
$('thead input[name="select_all"]', table.table().container()).on('click', function(e){
   if(this.checked){
      $('#mainTable tbody input[type="checkbox"]:not(:checked)').trigger('click');
   } else {
      $('#mainTable tbody input[type="checkbox"]:checked').trigger('click');
   }

   // Prevent click event from propagating to parent
   e.stopPropagation();
});

// Handle table draw event
table.on('draw', function(){
   // Update state of "Select all" control
   updateDataTableSelectAllCtrl(table);
});

// Handle form submission event
$('#frm-example').on('submit', function(e){
   var form = this;

   // Iterate over all selected checkboxes
   $.each(rows_selected, function(index, rowId){
      // Create a hidden element
      $(form).append(
          $('<input>')
             .attr('type', 'hidden')
             .attr('name', 'id[]')
             .val(rowId)
      );
   });
});

});
