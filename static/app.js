
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
    const chatSearch = document.getElementById("chat-search");
    const urlButton=document.getElementById("url-btn");
    let currentChatId = null;
    //LOADING DOCUMENTS IN THE LEFT PANEL
    async function loadDocuments(){
        const response=await fetch("/documents");
        const documents=await response.json();
        documentList.innerHTML="";
        documents.forEach(doc=>{
            const div=document.createElement("div");
            div.className="document-item";
            const title=document.createElement("span");
            title.className = "document-title";
            title.textContent=doc.filename;
            const deleteBtn=document.createElement("button");
            deleteBtn.innerHTML = '<i class="bi bi-trash"></i>';
            deleteBtn.className="document-delete";
            div.appendChild(title);
            div.appendChild(deleteBtn);
            documentList.appendChild(div);
            deleteBtn.addEventListener("click", async (e) => {
                e.stopPropagation();
                if (!confirm(`Delete "${doc.filename}"?`))
                    return;
                const response = await fetch(
                    `/delete_document/${doc.document_id}`,
                    {
                        method: "DELETE"
                    }
                );
                if(response.ok) {
                    await loadDocuments();
                }
                else{
                    alert("Failed to delete document.");
                }
            });
        });
    }
    //LOADING MESSAGES IN THE LEFT PANEL
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
    //LOADING MULTIPLE CHATS IN THE PANEL
    async function loadChats(activeChatId=null){
        const response=await fetch("/chats");
        const chats=await response.json();
        chatList.innerHTML="";
        chats.forEach(chat=>{
            const div=document.createElement("div");
            div.className="chat-item";
            div.dataset.id=chat.id
            if(chat.id===activeChatId){
                div.classList.add("active");
            }
            const title = document.createElement("span");
            title.className = "chat-title";
            title.textContent = chat.title;
            //RENAME AND DELETE MENU BUTTON FOR CHATS
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
                //RENAME OPTION
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
                    currentChatId = chat.id;
                    menu.remove();
                    await loadChats(currentChatId);
                });
                document.addEventListener(
                    "click",
                    () => menu.remove(),
                    { once: true }
                );
                //DELETE OPTION
                menu.querySelector(".delete-option").addEventListener("click", async (e) => {
                    e.stopPropagation();
                    const confirmDelete=confirm(`Delete "${chat.title}"?\n\nThis action cannot be undone.`);
                    if (!confirmDelete) return;
                    const response=await fetch(`/delete_chat/${chat.id}`,{method: "DELETE"});
                    if (response.ok){
                        menu.remove();
                        const result = await response.json();
                        currentChatId = result.current_chat;
                        await loadChats(currentChatId);
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
            //SWITCH CHAT
            div.addEventListener("click", async () => {
                currentChatId = chat.id;
                await fetch(`/switch_chat/${chat.id}`, {
                    method: "POST"
                });
                document
                    .querySelectorAll(".chat-item")
                    .forEach(item => item.classList.remove("active"));
                div.classList.add("active");
                loadDocuments();
                loadMessages();
                //console.log("Switched to", chat.title);
            });
            chatList.appendChild(div);
    });}
    //ADD MESSAGE 
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
    //UPLOAD BUTTON
    uploadButton.addEventListener("click",()=>{
        fileInput.click();
    });
    //TAKING DOCUMENTS AS INPUT
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
    //SEND BUTTON 
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
                    if(event.type==="sources" && event.data.length>0){
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
            await loadChats(currentChatId);
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
    //MESSAGE SENT BY PRESSING ENTER
    messageInput.addEventListener("keydown",(event)=>{
        if(event.key==="Enter"){
            event.preventDefault();
            button.click();
        }}
    );
    //NEW CHAT BUTTON
    newchatButton.addEventListener("click",async()=>{
        console.log("New Chat clicked");
        const response = await fetch("/new_chat",{
            method:"POST"
        });
        const result = await response.json();
        currentChatId = result.chat_id;
        await loadChats(currentChatId);
        await loadMessages();
        await loadDocuments();
    });
    loadChats(currentChatId);
    loadDocuments();
    loadMessages();
    //URL BUTTON
    urlButton.addEventListener("click",async ()=>{
        const url=prompt("Enter a url")
        if(!url) return;
        const response=await fetch("/add_url",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                url:url
            })
        });
        const result=await response.json();
        if (!response.ok) {
            alert(result.detail);
            return;
        }
        if(result.success){
            addMessage(`URL indexed successfully.\nIndexed ${result.chunks} chunks.`,"assistant");
            await loadDocuments();
        }
        else{
            alert("Failed.");
        }
    });
    chatSearch.addEventListener("input", ()=>{
        const search=chatSearch.value.toLowerCase();
        document.querySelectorAll(".chat-item").forEach(chat => {
            const title=chat.querySelector(".chat-title").textContent.toLowerCase();
            if (title.includes(search)) {
                chat.style.display = "";
            } else {
                chat.style.display = "none";
            }

        });

    });
});
