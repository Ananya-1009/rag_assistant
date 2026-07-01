
document.addEventListener("DOMContentLoaded",()=>{
    const button=document.getElementById("send-btn");
    const uploadButton=document.getElementById("upload-btn");
    const fileInput=document.getElementById("file-input");
    const messageInput=document.getElementById("message-input");
    const chatWindow=document.getElementById("chat-window");
    function addMessage(text,sender){
        const message=document.createElement("div");
        message.classList.add("message");
        message.classList.add(sender);
        message.textContent=text;
        chatWindow.appendChild(message);
        chatWindow.scrollTop=chatWindow.scrollHeight;
        return message;
    }
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
            if(result.success){
                addMessage(
                    `${result.filename} uploaded successfully.\nIndexed ${result.chunks} chunks.`,
                    "assistant"
                );
                fileInput.value="";
            }else{
                    addMessage(`${result.message}`,"assistant");
            }
        }catch(error){
            console.error(error);
            alert("Upload failed.");
        }
    });
    button.addEventListener("click",async()=>{
        const text=messageInput.value.trim();
        if(!text){
            return;
        }
        addMessage(text,"user");
        messageInput.value="";
        const thinkingMessage=addMessage("Thinking...","assistant");
        button.disabled = true;
        button.textContent = "Thinking...";
        try{
            const response=await fetch("/chat",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    question:text
                })
            });
            const result=await response.json();
            let responseText=result.answer;
            if(result.sources && result.sources.length>0){
                responseText+="\n\nSources:\n";
                const filenames=[...new Set(
                    result.sources.map(source=>source.filename)
                )];
                filenames.forEach(filename=>{
                    responseText+=`• ${filename}\n`;
                });
            }
            thinkingMessage.textContent=responseText;
            button.disabled=false;
            button.textContent="Send";
            messageInput.focus();
        }
        catch(error){
            console.error(error);
            thinkingMessage.innerHTML = `<strong>Error</strong>
            ${error.message}`;
            button.disabled = false;
            button.textContent = "Send";
            messageInput.focus();
        }
    });
    messageInput.addEventListener("keydown",(event)=>{
        if(event.key==="Enter"){
            event.preventDefault();
            button.click();
        }}
    );
});
