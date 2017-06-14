$(document).ready(function (){
  var workerlist = [];
  $("#selectbtn").click(function(){
      var target = "_blank";
      var url="";
      var content="";
      var id = 0;
      var group =document.getElementById("workergroup");
      while (group.hasChildNodes()) {
        group.removeChild(group.lastChild);
      }
      workerlist=[];
    $(".selected").each(function(){
      id++;
      $("<a"+" id=\"worker_"+ id + "\"target=\""+target+ "\"href=\"#\">&nbsp</a>").appendTo("#workergroup")
      content=$(this).find("td")[1].textContent;
      $("#worker_"+id).text(content);
      	$("#worker_"+id).attr("href","/accounts/"+content );
      $("#worker_"+id).append("   ");
      workerlist.push(content);
    });
    $("#worker_hidden").val(workerlist);
  });
});
