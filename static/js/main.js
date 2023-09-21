if(document.querySelector('#username')){
    // code to check the users names from the data base 
    usernameinput = document.getElementById('username')
    usernameinput.addEventListener('input' , ()=>{
        $.ajax({
            type:'GET',
            url:'check_username/'+usernameinput.value ,
            success:(res)=>{
                console.log(res);
                if(res.user != false || usernameinput.value.indexOf(" ") !== -1){
                    if(usernameinput.classList.contains('success')){
                        usernameinput.classList.remove('success')
                    }
                    usernameinput.classList.add('fail')
                    
                }else{
                    if(usernameinput.classList.contains('fail')){
                        usernameinput.classList.remove('fail')
                    }
                    usernameinput.classList.add('success')
                }
            }
        })
    })
    
}
if(document.getElementById('all-request')){
    cards = document.querySelectorAll('.card')
    // all requests 
    all_requrst = document.querySelector('#all-request').addEventListener('click' , ()=>{
        cards.forEach(e=>{
            e.style.display = "flex"
        })
    })
    // rejected filter
    reject = document.querySelector('#reject-request').addEventListener('click' , ()=>{
        cards.forEach(e => {
            if(e.querySelector('.rejected')){
                e.style.display = "flex";
            }else{
                e.style.display = "none";
            }
        });
    })

    // aproved requests 
    aproved = document.querySelector('#aprove-request').addEventListener('click' , ()=>{
        cards.forEach(e=>{
            if(e.querySelector('.aproved')){
                e.style.display = 'flex'
            }else{
                e.style.display = "none"
            }
        })
    })
}

// for the record and timer functions 

if(document.querySelector('.red-btn')){
    var hours =0;
    var mins =0;
    var seconds =0;
    var running = false

    
    $('.red-btn').click(function(){
        if(!running){
            startTimer();
            $('.red-btn').html("<h1> STOP </h1>")
            running = true
            $.ajax({
                type:"GET",
                url:"/requred",
                data:{'state':'running'}
            })
        }else{
            $('.red-btn').html("<h1> REC. </h1>")
            running = false
            clearTimeout(timex);
        }
    });
        
    $('.red-btn').dblclick(function(){
        hours =0;      mins =0;      seconds =0;
        $('#hours','#mins').html('00:');
        $('#seconds').html('00');
    });
    
    function startTimer(){
    timex = setTimeout(function(){
        seconds++;
        if(seconds >59){seconds=0;mins++;
            if(mins>59) {
            mins=0;hours++;
            if(hours <10) {$("#hours").text('0'+hours+':')} else $("#hours").text(hours+':');
            }               
        if(mins<10){                     
            $("#min").text('0'+mins+':');}       
            else $("#min").text(mins+':');
                    }    
        if(seconds <10) {
            $("#sec").text('0'+seconds);} else {
            $("#sec").text(seconds);
            }
        
        startTimer();
    },1000);
    }

    teachers = document.querySelectorAll(".teacher")
    teachers.forEach(e=>{
        e.addEventListener('click' , ()=>{
            $.ajax({
                type:"GET",
                url:"get_teacher/"+e.dataset.id,
                success:(res)=>{
                    document.querySelector('#teacher-name').innerText = res.teacher.name
                    document.querySelector('#teacher-image').src = 'media/'+ res.teacher.image
                }
            })
        })
    })


    search = document.getElementById('search')
    search.addEventListener('input' , ()=>{
        text = search.value
        teachers = document.querySelectorAll(".teacher")
        teachers.forEach( e=>{            
            if(e.innerText.toLowerCase().includes(text)){
                e.style.display = "flex"
            }else{
                e.style.display = "none"
            }
        })
    })

    subject = document.getElementById('subject')
    subject.addEventListener('change' , ()=>{
        text = subject.value
        teachers = document.querySelectorAll(".teacher")
        teachers.forEach(e=>{
            if(e.innerText.toLowerCase().includes(text.toLowerCase())){
                e.style.display = "flex"
            }else{
                e.style.display = "none"
            }
        })
    })

}