alert("Worked")
marked.setOptions({
    breaks: true,
    gfm: true
});

document.addEventListener("DOMContentLoaded",()=>{
    const newchatButton=document.getElementById("new-chat-btn");
    const chatList=document.getElementById("chat-list")
    const button=document.getElementById("send-btn");
    const uploadButton=document.getElementById("upload-btn");
    const fileInput=document.getElementById("file-input");
    const messageInput=document.getElementById("message-input");
    const chatWindow=document.getElementById("chat-window");
    const documentList =document.getElementById("document-list");
    async function loadDocuments(){
        const response=await fetch("/documents");
        const documents=await response.json();
        documentList.innerHTML="";
        documents.forEach(doc=>{
            const div=document.createElement("div");
            div.className="document-item";
            div.textContent=doc.filename;
            documentList.appendChild(div);
        });
    }
    async function loadMessages(){
        const response= await fetch("/messages");
        const messages=await response.json();
        chatWindow.innerHTML="";
        messages.forEach(message=>{
            addMessage(
                message.message,
                message.role
            );
        });
    }
    async function loadChats(){
        const response=await fetch("/chats");
        const chats=await response.json();
        chatList.innerHTML="";
        chats.forEach(chat=>{
        const div=document.createElement("div");
        div.className="chat-item";
        div.dataset.id=chat.id
        div.textContent=chat.title;
        div.addEventListener("click", async () => {
            await fetch(`/switch_chat/${chat.id}`, {
                method: "POST"
            });
            document
                .querySelectorAll(".chat-item")
                .forEach(item => item.classList.remove("active"));
            div.classList.add("active");
            loadDocuments();
            loadMessages();
            console.log("Switched to", chat.title);
        });
        chatList.appendChild(div);});
    }
    function addMessage(text, sender) {
        const message = document.createElement("div");
        message.classList.add("message");
        message.classList.add(sender);

        if (sender === "assistant") {
            message.innerHTML = marked.parse(text);
        } else {
            message.textContent = text;
        }

        chatWindow.appendChild(message);
        chatWindow.scrollTop = chatWindow.scrollHeight;

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
                loadDocuments();
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
        const thinkingMessage = addMessage("*Thinking...*", "assistant");
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
                responseText += "\n\n---\n\n";
                responseText += "### Sources\n\n";
                const filenames=[...new Set(
                    result.sources.map(source=>source.filename)
                )];
                filenames.forEach(filename=>{
                    responseText += `- ${filename}\n`;
                });
            }
            console.log(marked.parse(responseText));
            thinkingMessage.innerHTML=marked.parse(responseText);
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
    newchatButton.addEventListener("click",async()=>{
        console.log("New Chat clicked");
        await fetch("/new_chat",{
            method:"POST"
        });
        loadChats();
    });
    loadChats();
    loadDocuments();
    loadMessages();
});
