function buttonClick(button){
    let buttons = button.parentElement.querySelectorAll("button")
    if (buttons.length > 1){
        button.remove()
    }
    if(button.className == "red"){
        reject(button.value)
    }
    if(button.className == "green"){
        approve(button.value)
    }
}
cstoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;


function reject(id) {
  var button = document.getElementById("reject" + id);

  $.ajax({
    type: "POST",
    url: "/home_teamleader",
    headers: { "X-CSRFToken": cstoken },
    data: {
      toareject: id,
    },
    success:function(){
        button.classList.remove("red")
        button.classList.add("green")
        button.innerText = "Approve";
        button.id = "approve" + id;
    }
  });
   
}


function approve(id) {
  var button = document.getElementById("approve" + id);

  $.ajax({
    type: "POST",
    url: "/home_teamleader",
    headers: { "X-CSRFToken": cstoken },
    data: {
      toaprove: id
    },
    success:function(){
        button.classList.remove('green')
        button.classList.add('red')
        button.innerText = "Rejected";
        button.id = "reject" + id;
    }
  });
}

buttonsFilters = document.querySelectorAll(".section-head")
buttonsFilters.forEach(e => {
    e.addEventListener("click" , function(){
        // these for moving the line 
        var line = document.getElementById("LINE")
        line.style = `
        left:${e.offsetLeft - (e.offsetWidth + (e.offsetWidth/2))}px;
        width:${e.offsetWidth}px;
        `
        if(e.value == "Approve"){
            ApproveWork()
        }
        else if(e.value == "Rejected"){
            RejectedWork()
        }
        else if (e.value == "Employes"){
            Employes()
        }
    })
});

function ApproveWork(){
    $.ajax({
        type:"GET",
        url:"/filters",
        data:{
            "approve":true
        },
        success:function(html){
            document.querySelector(".grid-card").innerHTML = html
        }
    })
}

function RejectedWork(){
    $.ajax({
        type:"GET",
        url:"/filters",
        data:{
            "reject":true
        },
        success:function(html){
            document.querySelector(".grid-card").innerHTML=html
        }
    })
}

function Employes(){
    $.ajax({
        type:"GET",
        url:"/filters",
        data:{
            "Employes":true
        },
        success:function(html){
            document.querySelector(".grid-card").innerHTML=html
        }
    })
}