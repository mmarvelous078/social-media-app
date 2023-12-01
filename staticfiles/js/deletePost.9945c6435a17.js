var csrfToken = document.getElementById('csrf-form').querySelector('[name=csrfmiddlewaretoken]').value;

document.querySelectorAll('.ClickDeleteButtons').forEach(btn => {

    let postIds = btn.getAttribute('postId');
    
    document.getElementById(`deletePostBtn${postIds}`).addEventListener('click', ()=>{
        document.getElementById(`deleteButtonModal${postIds}`).style.display = 'flex'
    })

    document.getElementById(`AbortDeleteBtn${postIds}`).addEventListener('click', ()=>{
        document.getElementById(`deleteButtonModal${postIds}`).style.display = 'none'
    })

    const actualDeleteBtn = document.getElementById(`clickDeleteBtn${postIds}`);

    actualDeleteBtn.addEventListener('click', ()=>{
        console.log(postIds)
        const modalConfirmation = document.getElementById('confirmDeletionModal');

        modalConfirmation.classList.toggle('visible')
        document.getElementById('AbortDeletionModal').addEventListener('click',()=>{
            modalConfirmation.classList.remove('visible')
        })

        document.getElementById('ConfirmDeletionModal').addEventListener('click',()=>{
            document.getElementById(`deleteButtonModal${postIds}`).style.display = 'none'
            modalConfirmation.classList.toggle('visible')

            let xhrDelete = new XMLHttpRequest();
            xhrDelete.open('POST', `/delete_post/${postIds}`, true)
            xhrDelete.setRequestHeader("X-CSRFToken", csrfToken);
            xhrDelete.onreadystatechange = () => {
                if(xhrDelete.status === 200){
                    let response = JSON.parse(xhrDelete.responseText);

                    modalConfirmation.innerHTML = ''
                    modalConfirmation.classList.add('visible');

                    const messages = document.createElement('p')
                    messages.innerText = `${response.message}`

                    modalConfirmation.appendChild(messages);

                    setTimeout(()=>{
                        modalConfirmation.classList.remove('visible') 
                    },3000);

                    
                    console.log(response.message);
                    location.reload(true)
                    console.log('Post deleted Succesful');
                } else {
                    console.error('Error', xhrDelete.status, xhrDelete.statusText);
                }
            }
            xhrDelete.send()
        });
    });
});