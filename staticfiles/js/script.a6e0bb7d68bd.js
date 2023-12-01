const openButtons = document.querySelectorAll('.threeDotsButton')
const modal = document.getElementById('options')


openButtons.forEach(btn => {
    btn.addEventListener('click',()=>{
        let postId = btn.getAttribute('postIdAll')

        let pid = postId
        
        var xhr = new XMLHttpRequest();
        xhr.open('GET', `/home/options/${Number(postId)}`, true);
        xhr.onreadystatechange = () => {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                if(xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    var data = response

                    let singleData = data[0]

                    
                    let follow = document.getElementById('follow-username')
                    let mute = document.getElementById('mute-username')
                    let block_user = document.getElementById('block-username')

                    follow.innerHTML = `Follow ${singleData.owner}`
                    mute.innerHTML = `Mute ${singleData.owner}`
                    block_user.innerHTML = `Block ${singleData.owner}`

                    modal.style.display = 'block'
                    
                }else{
                    console.error('Error', xhr.status);
                }
            }
        };
        xhr.send();
    })
    var close = document.getElementsByClassName('close')[0];
    close.addEventListener('click', ()=>{
        modal.style.display = 'none';
    })

})


// --------------------------- Like System -------------------- //
const likebtns = document.querySelectorAll('.likebtns');

likebtns.forEach(
    btn => {
        btn.addEventListener('click',()=>{
            let postId = btn.getAttribute('postIdAll')
            const likeUpdater = document.getElementById(`likeCountSpan${postId}`)



            var xhr = new XMLHttpRequest();
            xhr.open('GET',`/likepost/${Number(postId)}`, true);
            xhr.onreadystatechange = () => {
                if(xhr.readyState === XMLHttpRequest.DONE){
                    if(xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        var data = response

                        likeUpdater.innerHTML = `${data.likes} likes`

                        if(data.is_liking === false) {
                            var lkicon = document.getElementById(`likeIconImge${postId}`)
                            lkicon.src = "static/svg/heart-regular.svg"
           
                        } else {
                            var lkicon = document.getElementById(`likeIconImge${postId}`)
                            lkicon.src = "static/svg/heart-solid.svg"

                        }

                    } else {
                        console.error('Error', xhr.status);
                    }
                }
            }
            xhr.send()
        });
    
    }
)
