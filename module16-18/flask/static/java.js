
// let value = [];
// function check(){
//   const request = XMLHttpRequest();
//   request.open('POST', '/api/search')
//   request.setRequestHeader("Content-Type", "application/json");
//   let search = document.querySelector('#Search').value;
//   if (search === ""){
//     Event.preventDefault();
//     return false;
//   }
//   if (document.querySelector('#drop').value == "ISBN"){
//     request.send(JSON.stringify({"searchby":"ISBN", "search": search}));
//   }else if (decodeURIComponent.querySelector('#drop').value == "Title"){
//     request.send(JSON.stringify({"searchby":"Title", "search":search}));
//   }else{
//     request.send(JSON.stringify({"searchby":"Author", "search": search}));
//   }
//   request.onload = () => {
//     const data = JSON.parse(request.responseText);
//     if (request.status === 400){
//       document.getElementById("panel-heading").innerHTML = "Showing "+0+" results for \""+search+"\"";
//   }else{
//     let isbns = data.isbns;
//     let titles = data.titles;
//     let authors = data.authors;
//     let string = "";
//     value = [];
//     for (let i = 0; i < isbns.length; i++){
//       value.push(isbns[i]);
//       string += "<tr>";
//       string += "<th scope=\"row\">"+(i+1)+"</th>";
//       string += "<td><a href=\"javascript:method("+i+")\">"+isbns[i]+"</a></td>";
//       string += "<td>"+titles[i]+"</td>";
//       string += "<td>"+authors[i]+"</td>";
//       string += "</tr>"
//     }
//     document.getElementById("panel-heading").innerHTML = "Showing "+isbns.length+" results for \""+search+"\"";
//     document.querySelector('#tbody').innerHTML = string;
//   }
//   document.getElementById("tableSection").style.display = "block";
//   document.getElementById("secondpart").style.display = "none";
//   Event.preventDefault();
//   return true;
// }
// }