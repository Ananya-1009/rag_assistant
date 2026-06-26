document.addEventListener("DOMContentLoaded",()=>{
    const button=document.getElementById("send-btn");
    const uploadButton=document.getElementById("upload-btn");
    const fileInput=document.getElementById("file-input");
    uploadButton.addEventListener("click",()=>{
        fileInput.click();
    });
    fileInput.addEventListener("change",async()=>{
        const file=fileInput.files[0];
        if(!file){
            return;
        }
        const formData=new FormData();
        formData.append("file",file);
        try{
            const response=await fetch("/upload",{
                method:"POST",
                body:formData
            });
            const result=await response.json();
            console.log(result);
            if(result.success){
                alert(result.message);
            }else{
                alert(result.message);
            }
        }catch(error){
            console.error(error);
            alert("Upload failed.");
        }
    });
    button.addEventListener("click",()=>{
        const input=document.getElementById("message-input");
        const text=input.value.trim();
        if(!text){
            return;
        }
        const chat=document.getElementById("chat-window");
        const div=document.createElement("div");
        div.className="message user";
        div.innerText=text;
        chat.appendChild(div);
        input.value="";
        chat.scrollTop=chat.scrollHeight;
    });
});