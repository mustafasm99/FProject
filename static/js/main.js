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