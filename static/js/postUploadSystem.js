document.getElementById('contentUploadForm').addEventListener('submit', (event)=>{
    event.preventDefault()

    let formName = document.querySelector('#contentUploadForm');

    let contentText = document.querySelector('input[name="content"]').value;
    let contentImage = document.querySelector('input[name="contentImage"]').files[0];

    if(contentText.trim() === '' || !contentImage) {
        alert('Please provide a title and select an Image.');
        return;
    }

    let formData = new FormData(formName);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/createPost/' ,true)
    xhr.onreadystatechange = () => {
        if(xhr.readyState === XMLHttpRequest.DONE){
            if(xhr.status === 200) {
                console.log('Upload sucessful');
                window.location.href = "/"
            } else {
                console.log('Error:', xhr.status, xhr.statusText);
            }
        }
    };
    xhr.send(formData);
});