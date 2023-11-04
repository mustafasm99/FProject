function All_works(){
    $.ajax({
        type:"GET",
        url:"/emp_filter",
        data:{
            "all":true
        },
        success:function(html){
            divs = document.querySelectorAll(".grid-card div")
            divs.forEach(e=>{
                e.style = "opacity: 0;"
                // e.remove()
            })
            setTimeout(function(){
                document.querySelector(".grid-card").innerHTML = html
            },400)
        }
    })
}
function ApproveWork(){
    $.ajax({
        type:"GET",
        url:"/emp_filter",
        data:{
            "approve":true
        },
        success:function(html){
            divs = document.querySelectorAll(".grid-card div")
            divs.forEach(e=>{
                e.style = "opacity: 0;"
                // e.remove()
            })
            setTimeout(function(){
                document.querySelector(".grid-card").innerHTML = html
            },400)
        }
    })
}

function RejectedWork(){
    $.ajax({
        type:"GET",
        url:"/emp_filter",
        data:{
            "reject":true
        },
        success:function(html){
            divs = document.querySelectorAll(".grid-card div")
            divs.forEach(e=>{
                e.style = "opacity: 0;"
                // e.remove()
            })
            setTimeout(function(){
                document.querySelector(".grid-card").innerHTML = html
            },400)
        }
    })
}

function NewWork(){
    $.ajax({
        type:"GET",
        url:"/emp_filter",
        data:{
            "NewWork":true
        },
        success:function(html){
            divs = document.querySelectorAll(".grid-card div")
            divs.forEach(e=>{
                e.style = "opacity: 0;"
                // e.remove()
            })
            setTimeout(function(){
                document.querySelector(".grid-card").innerHTML = html
            },400)
        }
    })
}

buttonsFilters = document.querySelectorAll(".section-head")
buttonsFilters.forEach(e => {
    e.addEventListener("click" , function(){
        // these for moving the line 
        var line = document.getElementById("LINE")
        line.style = `
        left:${e.offsetLeft - ((e.offsetWidth*1.5))}px;
        
        `
        if(e.value == "Approve"){
            ApproveWork()
        }
        else if(e.value == "Rejected"){
            RejectedWork()
        }
        else if (e.value == "NewWork"){
            NewWork()
        }
        else if (e.value == "all"){
            All_works()
        }
    })
});
