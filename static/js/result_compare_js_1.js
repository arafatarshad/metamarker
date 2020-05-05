
 $( document ).ready(function(){
 
      $("#job1_select").select2({
          placeholder: "Select a feature from the list",
          allowClear: true
      }); 
    $("#job2_select").select2({
          placeholder: "Select a feature from the list",
          allowClear: true
      }); 
        
 });

function all_panel_reset(){
 	$('#job1_select').val(null).trigger('change');
	$('#job2_select').val(null).trigger('change');
}