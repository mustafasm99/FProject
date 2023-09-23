if(document.querySelector('#username')){
    // code to check the users names from the data base 
    usernameinput = document.getElementById('username')
    usernameinput.addEventListener('input' , ()=>{
        $.ajax({
            type:'GET',
            url:'check_username/'+usernameinput.value ,
            success:(res)=>{
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

teacher_selected = false

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
        if(!teacher_selected){
            alert("يجب اختيار استاذ")
            return
        }
        if (document.getElementById('studio_page')) {
            if (!document.getElementById('studio_id').value) {
                alert("يجب اختيار ستوديو أولاً");
                return;
            }
            if (!document.getElementById('causes_id').value) {
                alert("يجب اختيار سبب التسجيل أولاً");
                return;
            }
        }
        if(!running){
            startTimer();
            $('.red-btn').html("<h1> STOP </h1>")
            running = true
            $.ajax({
                type:"GET",
                url:"/requred",
                data:{
                'state':'running' ,
                'teacher':document.getElementById('teacher_id').value,
                },
                success : (res)=>{
                    note = document.getElementById('note')
                    note.style = "opacity:1;"
                    note.style.display = "flex"
                    note.querySelector('div').innerHTML = `
                    <p> state : ${res.state} </p> <br> 
                    <p> start time : ${res.start_at} </p>
                    `
                }
            })
        }else{
            $('.red-btn').html("<h1> REC. </h1>")
            running = false
            restart()
            $.ajax({
                type:"GET",
                url:"/requred",
                data:{
                'state':'stop' ,
                'teacher':document.getElementById('teacher_id').value,
                'studio':document.getElementById('studio_id') ? document.getElementById('studio_id').value : '',
                'case':document.getElementById('causes_id') ? document.getElementById('causes_id').value : '',
                },
                success : (res)=>{
                    console.log(res);
                    note = document.getElementById('note')
                    note.style.display = "flex"
                    html = `
                    <p> state : ${res.state} </p> <br> 
                    <p> start time : ${res.start_time} </p> <br>
                    <p> end time : ${res.end_time} </p> <br>
                    <p> Total Time : ${res.Total_requred} </p>
                    `
                    if (res.cause){
                        html += `<p> Cause : ${res.cause} </p> <br>`
                    }
                    if (res.studio){
                        html += `<p> Studio : ${res.studio} </p> <br>`
                    }
                    note.querySelector('div').innerHTML = html
                }
            })
            clearTimeout(timex);
        }
    });
        
    function restart(){
        hours =0;      mins =0;      seconds =0;
        $('#hours','#mins').html('00:');
        $('#seconds').html('00');
    }
    
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

    // for the teacher click 
    teachers = document.querySelectorAll(".teacher")
    teachers.forEach(e=>{
        e.addEventListener('click' , ()=>{
            teacher_selected = true
            $.ajax({
                type:"GET",
                url:"get_teacher/"+e.dataset.id,
                success:(res)=>{
                    console.log(res);
                    document.querySelector('#teacher-name').innerText = res.teacher.name
                    document.querySelector('#teacher-image').src = 'media/'+ res.teacher.image
                    document.querySelector('#teacher_id').value = res.teacher.id
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

if(document.getElementById('aprovework')){
    aprovework.addEventListener('click' , ()=>{
        cards = document.querySelectorAll('.card')
        cards.forEach(e=>{
            if(e.querySelector('.aproved')){
                e.style = ' display:flex; '
            }else{
                e.style = ' display:none; '
            }
        })
    })
}

if(document.getElementById('rejectedwork')){
    rejectedwork.addEventListener('click' , ()=>{
        cards = document.querySelectorAll('.card')
        cards.forEach(e=>{
            if(e.querySelector('.rejected')){
                e.style = ' display:flex; '
            }else{
                e.style = ' display:none; '
            }
        })
    })
}

if(document.getElementById('all_work')){
    all_work.addEventListener('click' , ()=>{
        cards = document.querySelectorAll('.card')
        cards.forEach(e=>{
            e.style = ' display:flex; '
        })
    })
}

if(document.querySelector('.filter')){
    filters = document.querySelectorAll('.filter')
    filters.forEach(e=>{
        e.addEventListener('click' , (event)=>{
            if(e.classList.contains('btn-white')){
                filters.forEach(e=>{
                    e.classList.remove('label')
                    if (!e.classList.contains('btn-white')){
                        e.classList.add('btn-white')
                    }
                })
                e.classList.remove('btn-white')
                e.classList.add('label')

            }
        })
    })
}