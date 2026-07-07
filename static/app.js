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
        const title = document.createElement("span");
        title.className = "chat-title";
        title.textContent = chat.title;
        const menuBtn = document.createElement("button");
        menuBtn.className = "chat-menu";
        menuBtn.innerHTML = "⋮";
        div.appendChild(title);
        div.appendChild(menuBtn);
        menuBtn.addEventListener("click", (event) => {
            event.stopPropagation();
            const menu = document.createElement("div");
            menu.className = "chat-popup-menu";

            menu.innerHTML = `<div class="rename-option">Rename</div><div class="delete-option">Delete</div>`;
            div.appendChild(menu);
           
            menu.querySelector(".rename-option").addEventListener("click", async (e) => {
                e.stopPropagation();
                const newTitle = prompt("Rename chat",chat.title);
            if(!newTitle) return;
            await fetch(`/chats/${chat.id}`,{
                method:"PUT",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    title:newTitle})
                });
                menu.remove();
                await loadChats();
            });
            document.addEventListener(
                "click",
                () => menu.remove(),
                { once: true }
            );
            menu.querySelector(".delete-option").addEventListener("click", async (e) => {
                e.stopPropagation();
                const confirmDelete=confirm(`Delete "${chat.title}"?\n\nThis action cannot be undone.`);
                if (!confirmDelete) return;
                const response=await fetch(`/delete_chat/${chat.id}`,{method: "DELETE"});
                if (response.ok){
                    menu.remove();
                    const result = await response.json();
                    await loadChats();
                    document.querySelectorAll(".chat-item").forEach(item =>{
                        item.classList.remove("active");
                        if (item.dataset.id === result.current_chat) {
                            item.classList.add("active");
                        }
                    }); 
                    await loadMessages();
                    await loadDocuments();
                } 
                else {
                    alert("Failed to delete chat.");
                }
            });
        });
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
            const response=await fetch("/chat_stream",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    question:text
                })
            });
            const reader=response.body.getReader();
            const decoder=new TextDecoder();
            let answer="";
            let buffer="";
            while (true){
                const {done,value}=await reader.read();
                if(done) break;
                buffer+=decoder.decode(value);
                const lines=buffer.split("\n");
                buffer=lines.pop();
                for(const line of lines){
                    if (!line.trim()) continue;
                    const event=JSON.parse(line);
                    if(event.type==="token"){
                        answer += event.content;
                        thinkingMessage.innerHTML=marked.parse(answer);
                    }
                    if(event.type==="sources"){
                        answer+="\n\n---\n\n";
                        answer+="### Sources\n\n";
                        event.data.forEach(file=>{
                            answer+=`- ${file}\n`;
                        });
                        thinkingMessage.innerHTML=marked.parse(answer);
                    }
                } 
                chatWindow.scrollTop=chatWindow.scrollHeight;
            }
            await loadChats();
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
